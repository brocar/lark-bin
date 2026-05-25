# Maintainer: Your Name <your.email@example.com>
# Based on feishu-bin by Allen Zhong, Xuanwo, and Zhou Zhiqiang
pkgname=lark-bin
pkgver=7.66.10
_pkgtyp=stable
pkgrel=1
pkgdesc="Linux client of Lark (Feishu) from Bytedance."
arch=('x86_64' 'aarch64')
url="https://www.larksuite.com/"
license=('unknown')
depends=('alsa-lib' 'ca-certificates' 'gtk3' 'libappindicator-gtk3' 'libglvnd' 'nss' 'xdg-utils')
makedepends=('curl')
conflicts=('lark' 'larksuite-bin')
provides=('lark' 'bytedance-lark')
options=('!strip' '!emptydirs')
install=lark-bin.install
source_x86_64=(Lark-linux_x64-${pkgver}.deb::https://www.larksuite.com/api/package_info?platform=10)
source_aarch64=(Lark-linux_arm64-${pkgver}.deb::https://www.larksuite.com/api/package_info?platform=11)
DLAGENTS=("https::/usr/bin/bash ${startdir}/dlagent.sh %o %u")
sha256sums_x86_64=('0561e2e29a55550743afe8c2907eaf2289b23646744865c80f28352f80771eba')
sha256sums_aarch64=('b28ef0fd5c4d10e319738fae79214721f4a047a325d9c33d014e8982a60bb3ab')

package(){
  # Extract package data
  tar xpvf "${srcdir}/data.tar.xz" --xattrs-include='*' --numeric-owner -C "${pkgdir}"

  # Modify files
  cd "${pkgdir}"
  cat << EOF > usr/bin/lark
#!/bin/bash

XDG_CONFIG_HOME=\${XDG_CONFIG_HOME:-~/.config}

# Allow users to override command-line options
if [[ -f \$XDG_CONFIG_HOME/lark-flags.conf ]]; then
    LARK_USER_FLAGS="\$(grep -v '^#' \$XDG_CONFIG_HOME/lark-flags.conf)"
fi

# Launch
exec /usr/bin/bytedance-lark-${_pkgtyp} \$LARK_USER_FLAGS "\$@"
EOF

  chmod +x usr/bin/lark

  sed -i "s/bytedance-lark-${_pkgtyp}/lark/g" "${pkgdir}/usr/share/applications/bytedance-lark.desktop"
  sed -i 's/StartupNotify=true/StartupNotify=true\nStartupWMClass=lark/g' "${pkgdir}/usr/share/applications/bytedance-lark.desktop"

  sed -i "s/bytedance-lark-${_pkgtyp}/lark/g" "${pkgdir}/usr/share/menu/bytedance-lark.menu"
  sed -i "s/bytedance-lark/lark/g" "${pkgdir}/usr/share/menu/bytedance-lark.menu"

  sed -i 's/bytedance-lark/lark/g' "${pkgdir}/usr/share/appdata/bytedance-lark.appdata.xml"

  sed -i 's/bytedance-lark/lark/g' "${pkgdir}/opt/bytedance/lark/bytedance-lark"

  mv "${pkgdir}"/usr/share/menu/{bytedance-,}lark.menu
  mv "${pkgdir}"/usr/share/applications/{bytedance-,}lark.desktop
  mv "${pkgdir}"/usr/share/appdata/{bytedance-,}lark.appdata.xml
  mv "${pkgdir}"/usr/share/man/man1/{bytedance-lark-${_pkgtyp},lark}.1.gz
  mv "${pkgdir}"/usr/share/doc/{bytedance-lark-${_pkgtyp},lark}

  # Fix directory permissions
  find "${pkgdir}" -type d | xargs chmod 755
}
