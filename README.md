# SecureCert

SecureCert is a simple blockchain-based project designed to securely store and verify certificates. The main idea behind this project is to avoid fake or tampered certificates by using blockchain technology.

## About the Project

In many cases, certificates can be easily forged or modified. This project tries to solve that problem by storing certificate data in a blockchain structure, where each record is linked and cannot be changed without affecting the entire chain.

This makes the system more secure and trustworthy.

## Features

- Add new certificates to the blockchain
- Verify if a certificate is valid or not
- Tamper-proof data storage
- Simple and easy-to-understand implementation

## How it Works

Each certificate is stored as a block.  
Every block contains:
- Certificate details
- Hash of the previous block
- Its own unique hash

Because of this linking, if someone tries to change data, the chain becomes invalid.

## Tech Used

- JavaScript / Node.js (or your tech stack)
- Basic blockchain logic (hashing + chaining)

## How to Run

1. Clone the repository  
   ```bash
   git clone https://github.com/your-username/SecureCert.git
