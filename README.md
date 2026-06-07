# Project 3: ERC-20 Token Wallet & Value Transfer
**Batch: 2026 | Powered by DecodeLabs**[cite: 3]

## 📌 Project Overview
This application shifts focus to the "Nervous System of DeFi"[cite: 3]. Moving digital assets is not just a simple database update; it requires deterministic on-chain state updates and airtight logic[cite: 3]. By standardizing assets through the ERC-20 blueprint, we ensure seamless interoperability across the ecosystem[cite: 3]. This Python simulation models both the frontend input sanitization and the strict backend ledger manipulation.

---

## 🏗️ Banking Logic: The IPO Architecture
A secure token wallet is built on the Input-Process-Output (IPO) framework[cite: 3].

### 1. The INPUT Phase (Secure Data Acquisition)
Garbage in, garbage out[cite: 3]. If input is malformed, processing will fail.
* **Target Address Validation:** We utilize regex validation for the `0x` format to prevent copy-paste errors and malicious redirection[cite: 3].
* **Transfer Amount Sanity:** We check for non-negative values to prevent UI-level logic errors before they reach the blockchain[cite: 3].

### 2. The PROCESS Phase (The State Manipulation Engine)
The deterministic core applies strict, sequential financial logic to update the private ledger (BalancesMapper)[cite: 3].
* **Authorization / Overdraft Prevention:** The script enforces `require(balance >= amount)` to explicitly stop the spending of non-existent funds[cite: 3].
* **Underflow Protection:** The logic utilizes built-in math checks to prevent numbers from wrapping around and creating infinite money[cite: 3].
* **State Change:** We subtract the exact amount from the sender and add it to the recipient, ensuring encapsulated state variables apply the financial rules without exception[cite: 3].

### 3. The OUTPUT Phase (Data Integrity)
A transaction completes by ensuring ecosystem synchronization[cite: 3].
* The system executes a permanent state change on the internal ledger[cite: 3].
* An event (`Transfer(from, to, value)`) is emitted, which is crucial for block explorers, indexers, and off-chain analytics[cite: 3].

---

## ⚠️ The Double-Precision Paradox
This project specifically addresses the scale mismatch between frontends and the blockchain ledger[cite: 3].

* **The Trap:** JavaScript natively uses 64-bit IEEE 754 double-precision floating-point numbers, which lose precision beyond ~15 digits (53 bits)[cite: 3].
* **The Danger:** Naively converting a 256-bit EVM balance into a native JS Number results in rounding errors, which translates to a catastrophic loss of institutional funds[cite: 3]. 

To convert backend EVM integers for a UI, the formula is:
$UserReadable = \frac{InternalInteger}{10^{decimals}}$[cite: 3]

### The BigNumber Solution
To bypass floating-point limitations entirely, standard ERC-20 implementations utilize fixed-point arithmetic[cite: 3]. In this Python implementation, we simulate the `ethers.js` BigNumber approach by converting user string inputs directly into massive raw integers (scaling them by $10^{18}$), preventing fractional data loss entirely[cite: 3].


### OUTPUT
Initializing DecodeLabs Node...

Vault Admin Balance: 1000.0 Tokens

⚡ Initiating transfer of 50.5 Tokens...
🔗 [EVENT EMITTED] Transfer: 50500000000000000000 raw units from 0xAdmin00000000000000000000000000000000000 to 0xUser11111111111111111111111111111111111
✅ Transaction Successful! UI Synchronized.

⚡ Initiating transfer of 10 Tokens...
❌ Security Checkpoint Triggered: Malformed Data: Invalid 0x Address format.

⚡ Initiating transfer of 9000 Tokens...
❌ Security Checkpoint Triggered: Overdraft: Insufficient funds.

--- FINAL LEDGER BALANCES ---
Admin Vault: 949.5 Tokens
User Wallet: 50.5 Tokens