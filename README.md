# Lark (Arch Linux AUR package)

## Important: Unofficial

This is **not an official** Lark/Feishu/ByteDance repository, and it is **not affiliated with or endorsed by ByteDance**.

This repository exists to maintain an **Arch Linux AUR package** for the Lark desktop app.

## What is this?

Lark is the international (non‑China) version of Feishu, a ByteDance product.

- This repo contains **packaging files** (e.g., `PKGBUILD`) used by Arch Linux users to install Lark via the AUR.
- It does **not** contain Lark’s source code.

## Install (from this git repo)

This is the “manual AUR” method: you clone the packaging files and build/install the package locally.

Clone this repository and install:
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ./install.sh
   ```

## Update (from this git repo)

From inside your cloned folder:

```bash
./install.sh
```

## Uninstall

Once installed, it behaves like a normal package. For example:

```bash
sudo pacman -Rns lark-bin
```
