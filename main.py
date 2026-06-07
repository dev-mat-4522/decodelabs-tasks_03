class DecodeToken:
    """
    Project 3: ERC-20 Token Wallet & Value Transfer
    Encapsulating state variables ensures that all financial rules 
    are applied to every transaction without exception.
    """
    def __init__(self, initial_supply, deployer_address):
        # The Private Ledger: mapping(address => uint256)
        self.__balances = {}
        self.__balances[deployer_address] = initial_supply
        
        # The EVM tracks balances as large integers using the decimals variable
        self.decimals = 18

    def balance_of(self, owner_address):
        """Returns the exact token balance without modifying the ledger."""
        return self.__balances.get(owner_address, 0)

    def transfer(self, sender_address, target_address, amount):
        """State-mutating, logic-heavy core engine for moving value."""
        
        # INPUT PHASE: Target Address Validation
        if not target_address or not target_address.startswith("0x"):
            raise ValueError("Malformed Data: Invalid 0x Address format.")
            
        # INPUT PHASE: Transfer Amount Sanity
        if amount < 0:
            raise ValueError("Invalid Amount: Cannot send negative tokens.")
            
        # PROCESS PHASE: Authorization / Overdraft Check
        sender_balance = self.balance_of(sender_address)
        if sender_balance < amount:
            raise ValueError("Overdraft: Insufficient funds.")
            
        # PROCESS PHASE: State Subtraction Logic
        self.__balances[sender_address] = sender_balance - amount
        self.__balances[target_address] = self.balance_of(target_address) + amount
        
        # OUTPUT PHASE: Event Emission
        self._emit_transfer_event(sender_address, target_address, amount)
        return True

    def _emit_transfer_event(self, sender, to, value):
        print(f"🔗 [EVENT EMITTED] Transfer: {value} raw units from {sender} to {to}")


# ==========================================
# FRONTEND SIMULATION: The Scale Mismatch Solution
# ==========================================
def secure_transfer(sender_address, target_address, amount_string, token_contract):
    """
    Handles the Double-Precision Paradox by converting human-readable strings 
    into 256-bit fixed-point integers before executing the transfer.
    """
    try:
        # Convert user-readable string to an internal integer using 18 decimals
        safe_amount = int(float(amount_string) * (10 ** token_contract.decimals))
        
        print(f"\n⚡ Initiating transfer of {amount_string} Tokens...")
        
        # Execute the Smart Contract logic
        token_contract.transfer(sender_address, target_address, safe_amount)
        
        print("✅ Transaction Successful! UI Synchronized.")
        
    except ValueError as e:
        # This catches our security barriers (like invalid addresses or overdrafts)
        print(f"❌ Security Checkpoint Triggered: {e}")
    except Exception as e:
        print(f"❌ System Error: {e}")


# ==========================================
# SYSTEM RUNNER & THREAT DIAGNOSTICS
# ==========================================
if __name__ == "__main__":
    print("Initializing DecodeLabs Node...\n")
    
    # 1. Setup Data
    deployer = "0xAdmin00000000000000000000000000000000000"
    recipient = "0xUser11111111111111111111111111111111111"
    
    # Mint 1,000 tokens (with 18 decimals) to the deployer
    initial_supply = 1000 * (10 ** 18)
    decode_token = DecodeToken(initial_supply, deployer)
    
    print(f"Vault Admin Balance: {decode_token.balance_of(deployer) / (10**18)} Tokens")

    # ---------------------------------------------------------
    # Test 1: Successful Enterprise-Grade Transfer
    # ---------------------------------------------------------
    secure_transfer(
        sender_address=deployer,
        target_address=recipient,
        amount_string="50.5",
        token_contract=decode_token
    )
    
    # ---------------------------------------------------------
    # Test 2: Threat Diagnostic - Malformed Data (No 0x prefix)
    # ---------------------------------------------------------
    secure_transfer(
        sender_address=deployer,
        target_address="HackerAddress",
        amount_string="10",
        token_contract=decode_token
    )
    
    # ---------------------------------------------------------
    # Test 3: Threat Diagnostic - Overdraft (Insufficient Funds)
    # ---------------------------------------------------------
    # Recipient only has 50.5 tokens, attempting to send 9000
    secure_transfer(
        sender_address=recipient,
        target_address=deployer,
        amount_string="9000",
        token_contract=decode_token
    )

    # ---------------------------------------------------------
    # Final Output Sync
    # ---------------------------------------------------------
    print("\n--- FINAL LEDGER BALANCES ---")
    print(f"Admin Vault: {decode_token.balance_of(deployer) / (10**18)} Tokens")
    print(f"User Wallet: {decode_token.balance_of(recipient) / (10**18)} Tokens")