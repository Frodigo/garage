---
date: 2025-03-28
---

Adopted in 1977 by the National Bureau of Standards,

Data are encrypted in 64 bits blocks using 56 bit key.

Algorithm[^1] transforms input in a series of steps to output with the same 64 bit length.

The same steps and keys are used for decryption

terms:

- **Feistel Structure** - A network architecture in which data is divided into two parts, and only one part is modified in each round.
- **S-boxes (Substitution boxes)** - Substitution tables converting 6-bit inputs to 4-bit outputs, introducing non-linearity to the algorithm.
- **E Expansion** - A function expanding 32-bit input to 48 bits by repeating certain bits.
- **Subkeys** - A set of 16 derivative keys, generated from the master key, used in consecutive rounds.
- **PC-1 and PC-2 Permutations** - Special permutations used in the subkey generation process.
- **Key Parity Bits** - In the original 64-bit DES key, every eighth bit is a parity bit used to verify key correctness.

---

[^1]: [[Cryptography and network security principles and practice (fifth edition) by William Stallings]]
