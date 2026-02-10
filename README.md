# Lark AUR Package - Automated Updates

This repository contains the AUR package for Lark Suite with automated daily version checking via GitHub Actions.

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── aur-update.yml          # GitHub Actions workflow
├── aur/                            # AUR package files
│   ├── PKGBUILD
│   ├── .SRCINFO
│   ├── dlagent-lark.sh
│   └── lark-bin.install
└── update_ver.py                   # Version checker script
```

## How It Works

1. **Daily Check**: GitHub Actions runs daily at 8am UTC (configurable in the workflow)
2. **Version Detection**: `update_ver.py` queries the Lark API for the latest version
3. **Checksum Calculation**: Downloads both x86_64 and aarch64 binaries to calculate SHA256 sums
4. **Update PKGBUILD**: If a new version is found, updates `pkgver`, `pkgrel`, and checksums
5. **Generate .SRCINFO**: Uses `makepkg --printsrcinfo` to regenerate metadata
6. **Push to GitHub**: Commits changes to this repository
7. **Push to AUR**: Clones the AUR repository and pushes the updated package files

## Setup Instructions

### 1. Configure GitHub Repository

1. **Add AUR SSH Key as Secret**:
   - Generate an SSH key pair (if you don't have one):
     ```bash
     ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/aur
     ```
   - Add the public key (`~/.ssh/aur.pub`) to your [AUR account](https://aur.archlinux.org/account)
   - In GitHub: Go to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   - Name: `AUR_SSH_PRIVATE_KEY`
   - Value: Paste the contents of `~/.ssh/aur` (the private key)

2. **Enable GitHub Actions**:
   - Go to **Settings** → **Actions** → **General**
   - Ensure "Allow all actions and reusable workflows" is selected
   - Under "Workflow permissions", select "Read and write permissions"

### 2. Test the Workflow

Manually trigger the workflow to test:
- Go to **Actions** → **Update AUR Package** → **Run workflow**

### 3. Customize Schedule (Optional)

Edit [.github/workflows/aur-update.yml](.github/workflows/aur-update.yml) to change the check frequency:

```yaml
on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8am UTC
    # Examples:
    # - cron: '0 */6 * * *'  # Every 6 hours
    # - cron: '0 0 * * 1'    # Weekly on Monday
```

## Manual Version Update

To manually check for updates and update the package:

```bash
# Run the update script
python update_ver.py

# Generate .SRCINFO
cd aur
makepkg --printsrcinfo > .SRCINFO

# Commit and push
git add aur/PKGBUILD aur/.SRCINFO
git commit -m "Update to version X.Y.Z"
git push
```

## Troubleshooting

### Workflow Fails on .SRCINFO Generation

Ensure the PKGBUILD syntax is correct:
```bash
cd aur
namcap PKGBUILD
```

### SSH Key Issues

Verify your SSH key is properly configured:
```bash
ssh -T aur@aur.archlinux.org
```

You should see: "Hi [username]! You've successfully authenticated..."

### Version Not Updating

Check the workflow logs in the **Actions** tab. Common issues:
- API endpoint changes
- Network connectivity issues
- PKGBUILD syntax errors

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

See the PKGBUILD for package license information.
