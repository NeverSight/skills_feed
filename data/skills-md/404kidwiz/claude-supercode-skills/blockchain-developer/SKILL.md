---
name: blockchain-developer
description: Expert in Web3 development, smart contracts (Solidity/Rust), and decentralized application (dApp) architecture.
---

# Blockchain Developer

## Purpose

Provides Web3 development expertise specializing in smart contracts (Solidity/Rust), decentralized application (dApp) architecture, and blockchain security. Builds secure smart contracts, optimizes gas usage, and integrates with Layer 2 scaling solutions (Arbitrum, Optimism, Base).

## When to Use

- Writing and deploying Smart Contracts (ERC-20, ERC-721, ERC-1155)
- Auditing contracts for security vulnerabilities (Reentrancy, Overflow)
- Integrating dApp frontends with wallets (MetaMask, WalletConnect, RainbowKit)
- Building DeFi protocols (AMMs, Lending, Staking)
- Implementing Account Abstraction (ERC-4337)
- Indexing blockchain data (The Graph, Ponder)

---
---

## 2. Decision Framework

### Blockchain Network Selection

```
Which chain fits the use case?
│
├─ **Ethereum L1**
│  ├─ High value transactions? → **Yes** (Max security)
│  └─ Cost sensitive? → **No** (High gas fees)
│
├─ **Layer 2 (Arbitrum / Optimism / Base)**
│  ├─ General purpose? → **Yes** (EVM equivalent)
│  ├─ Low fees? → **Yes** ($0.01 - $0.10)
│  └─ Security? → **High** (Inherits from Eth L1)
│
├─ **Sidechains / Alt L1 (Polygon / Solana / Avalanche)**
│  ├─ Massive throughput? → **Solana** (Rust based)
│  └─ EVM compatibility? → **Polygon/Avalanche**
│
└─ **App Chains (Cosmos / Polkadot / Supernets)**
   └─ Need custom consensus/gas token? → **Yes** (Sovereignty)
```

### Development Stack (2026 Standards)

| Component | Recommendation | Why? |
|-----------|----------------|------|
| **Framework** | **Foundry** | Rust-based, blazing fast tests, Solidity scripting. (Hardhat is legacy). |
| **Frontend** | **Wagmi + Viem** | Type-safe, lightweight replacement for Ethers.js. |
| **Indexing** | **Ponder / The Graph** | Efficient event indexing. |
| **Wallets** | **RainbowKit / Web3Modal** | Best UX, easy integration. |

**Red Flags → Escalate to `security-auditor`:**
- Contract holds > $100k value without an audit
- Using `delegatecall` with untrusted inputs
- Implementing custom cryptography (Rolling your own crypto)
- Upgradable contracts without a Timelock or Multi-sig governance

---
---

## 4. Core Workflows

### Workflow 1: Smart Contract Development (Foundry)

**Goal:** Create a secure ERC-721 NFT contract with whitelist.

**Steps:**

1.  **Setup**
    ```bash
    forge init my-nft
    forge install OpenZeppelin/openzeppelin-contracts
    ```

2.  **Contract (`src/MyNFT.sol`)**
    ```solidity
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.20;

    import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
    import "@openzeppelin/contracts/access/Ownable.sol";
    import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

    contract MyNFT is ERC721, Ownable {
        bytes32 public merkleRoot;
        uint256 public nextTokenId;

        constructor(bytes32 _merkleRoot) ERC721("MyNFT", "MNFT") Ownable(msg.sender) {
            merkleRoot = _merkleRoot;
        }

        function mint(bytes32[] calldata proof) external {
            bytes32 leaf = keccak256(abi.encodePacked(msg.sender));
            require(MerkleProof.verify(proof, merkleRoot, leaf), "Not whitelisted");
            
            _safeMint(msg.sender, nextTokenId);
            nextTokenId++;
        }
    }
    ```

3.  **Test (`test/MyNFT.t.sol`)**
    ```solidity
    function testMintWhitelist() public {
        // Generate Merkle Tree in helper...
        bytes32[] memory proof = tree.getProof(user1);
        
        vm.prank(user1);
        nft.mint(proof);
        
        assertEq(nft.ownerOf(0), user1);
    }
    ```

---
---

### Workflow 3: Gas Optimization Audit

**Goal:** Reduce transaction costs for users.

**Steps:**

1.  **Analyze Storage**
    -   Pack variables: `uint128 a; uint128 b;` fits in one slot (32 bytes).
    -   Use `constant` and `immutable` for fixed values.

2.  **Code Refactoring**
    -   Use `custom errors` instead of string `require` messages (saves ~gas).
    -   Cache array length in loops (`unchecked { ++i }`).
    -   Use `calldata` instead of `memory` for function arguments where possible.

3.  **Verification**
    -   Run `forge test --gas-report`.

---
---

## 4. Patterns & Templates

### Pattern 1: Checks-Effects-Interactions (Security)

**Use case:** Preventing Reentrancy attacks.

```solidity
function withdraw() external {
    // 1. Checks
    uint256 balance = userBalances[msg.sender];
    require(balance > 0, "No balance");

    // 2. Effects (Update state BEFORE sending ETH)
    userBalances[msg.sender] = 0;

    // 3. Interactions (External call)
    (bool success, ) = msg.sender.call{value: balance}("");
    require(success, "Transfer failed");
}
```

### Pattern 2: Transparent Proxy (Upgradability)

**Use case:** Upgrading contract logic while keeping state/address.

```solidity
// Implementation V1
contract LogicV1 {
    uint256 public value;
    function setValue(uint256 _value) external { value = _value; }
}

// Proxy Contract (Generic)
contract Proxy {
    address public implementation;
    function upgradeTo(address _newImpl) external { implementation = _newImpl; }
    
    fallback() external payable {
        address _impl = implementation;
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), _impl, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
```

### Pattern 3: Merkle Tree Whitelist (Gas Efficient)

**Use case:** Whitelisting 10,000 users without storing them on-chain.

-   **Off-chain:** Hash all addresses -> Root Hash.
-   **On-chain:** Store only Root Hash (32 bytes).
-   **Verification:** User provides Proof (path to root). Cost is O(log n), very cheap.

---
---

## 6. Integration Patterns

### **backend-developer:**
-   **Handoff**: Blockchain dev provides ABI and Contract Address → Backend uses Alchemy/Infura to listen for events.
-   **Collaboration**: Indexing strategy (The Graph vs Custom SQL indexer).
-   **Tools**: Alchemy Webhooks, Tenderly.

### **frontend-ui-ux-engineer:**
-   **Handoff**: Blockchain dev provides wagmi hooks → Frontend builds UI.
-   **Collaboration**: Handling loading states, transaction confirmations, and error toasts ("User rejected request").
-   **Tools**: RainbowKit.

### **security-auditor:**
-   **Handoff**: Blockchain dev freezes code → Auditor reviews.
-   **Collaboration**: Fixing findings (Critical/High/Medium).
-   **Tools**: Slither, Mythril.

---
