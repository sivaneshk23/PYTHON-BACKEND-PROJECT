# SecureBank - Week 2 Testing

## Test Date

03/08/2026

## Features Tested

The following Week 2 features were tested successfully.

### Test 1 - Account Creation

Created two accounts with valid initial balances.

Result: PASS

### Test 2 - Money Transfer

Transferred money from one valid account to another.

Verified that:

- Sender balance decreased correctly
- Receiver balance increased correctly

Result: PASS

### Test 3 - Transfer Reversal

Reversed the sender's previous transfer.

Verified that:

- Money was returned to the sender
- Money was removed from the receiver
- Original balances were restored

Result: PASS

### Test 4 - Transaction History

Verified transaction history after transfer and reversal.

The original transfer transactions were preserved and marked as reversed.

Reversal transactions were also recorded.

Result: PASS

### Test 5 - Insufficient Balance During Transfer Reversal

Tested transfer reversal after the receiver no longer had enough money to return the transferred amount.

The system rejected the reversal without partially modifying either account.

Result: PASS

### Test 6 - Same Account Transfer

Attempted to transfer money from an account to the same account.

The system rejected the operation.

Result: PASS

## Final Result

All planned Week 2 Day 2 test cases passed successfully.

The system now supports safer transaction reversal while preserving transaction history.