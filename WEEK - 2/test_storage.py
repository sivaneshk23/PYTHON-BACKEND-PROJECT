from storage_manager import (
    load_data,
    save_data
)


sample = {
    "next_account_id": 10,
    "accounts": [],
    "transactions": []
}

save_data(sample)

loaded = load_data()

assert loaded == sample

print("Storage test: PASS")