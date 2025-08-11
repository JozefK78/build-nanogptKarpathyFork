from datasets import load_dataset
import tiktoken
import numpy as np
import multiprocessing as mp
import os

# Parameters
dataset_name = "HuggingFaceH4/FineWeb"
shard_size = 100_000_000
out_dir = "shards"
os.makedirs(out_dir, exist_ok=True)
num_workers = 8

# Tokenizer (needs to be re-created in each subprocess)
def encode_text(text):
    enc = tiktoken.get_encoding("gpt2")
    return enc.encode(text)

def shard_writer(token_queue, stop_event):
    all_tokens = []
    shard_idx = 0
    while not stop_event.is_set() or not token_queue.empty():
        try:
            tokens = token_queue.get(timeout=1)
            all_tokens.extend(tokens)
            while len(all_tokens) >= shard_size:
                shard = np.array(all_tokens[:shard_size], dtype=np.uint16)
                np.save(f"{out_dir}/shard_{shard_idx:05d}.npy", shard)
                print(f"Saved shard_{shard_idx:05d}.npy")
                shard_idx += 1
                all_tokens = all_tokens[shard_size:]
        except:
            continue

    # Final flush
    if all_tokens:
        shard = np.array(all_tokens, dtype=np.uint16)
        np.save(f"{out_dir}/shard_{shard_idx:05d}.npy", shard)
        print(f"Saved final shard_{shard_idx:05d}.npy")

def main():
    ds = load_dataset(dataset_name, split="train", streaming=True)

    token_queue = mp.Queue(maxsize=100)
    stop_event = mp.Event()
    writer = mp.Process(target=shard_writer, args=(token_queue, stop_event))
    writer.start()

    with mp.Pool(num_workers) as pool:
        for encoded in pool.imap_unordered(encode_text, (item["text"] for item in ds), chunksize=10):
            token_queue.put(encoded)

    stop_event.set()
    writer.join()

if __name__ == "__main__":
    main()
