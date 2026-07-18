# Arch packages

计划结构：

```text
kernel/linux-uconsole/
platform/uconsole-platform/
firstboot/uconsole-firstboot/
desktop/uconsole-desktop-sway/
```

所有 package 使用原生 PKGBUILD 和 pacman hooks。Ubuntu `.deb`、Debian
maintainer scripts 与 `flash-kernel` 仅可作为行为参考，不能直接安装。

Package validation 必须覆盖：

- package identity、version、architecture 和 file ownership；
- install/upgrade/remove；
- 前一 kernel ABI 共存；
- mkinitcpio 与 boot slot 更新；
- 不拥有任意 `/home/*`；
- 不包含 credential、host path 或 signing private key。
