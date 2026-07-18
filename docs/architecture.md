# 架构

## 设计原则

Arch Linux ARM 与 Ubuntu 共用硬件事实和 kernel source lineage，但不共用
distribution packaging。`.deb`、Debian maintainer scripts、`flash-kernel`
和 Ubuntu initramfs hooks 不得直接安装到 Arch rootfs。

## 分层

```text
Signed Arch Linux ARM rootfs
             │
             ▼
Pinned pacman package set ──► uconsole platform packages
             │                          │
             ▼                          ▼
      Arch image composer       boot policy / diagnostics
             │                          │
             └──────────┬───────────────┘
                        ▼
          Raspberry Pi firmware direct boot
                        │
                        ▼
      linux-uconsole + DTB/overlays + mkinitcpio
                        │
                        ▼
             CM4 Lite hardware validation
```

## Rootfs

- 输入采用 Arch Linux ARM 的 AArch64 Raspberry Pi rootfs。
- manifest 固定 filename、URL、archive SHA、signature URL、signing key 和
  package database state。
- 解包后首先验证并移除默认 `alarm` 账户，锁定不用于登录的 root account。
- image compose 不导入 host `/home`、machine-id、SSH host keys 或认证状态。

Arch Linux ARM 是 rolling distribution。可重现 release 不能依赖浮动
`pacman -Syu`；构建必须保存 exact package lock、package SHA 和可恢复的本地
package archive。

## Kernel

- source 只来自 `blue-1ms/rpi-linux` 的 exact commit。
- 本仓库维护 Arch-specific config fragment、patch inventory、PKGBUILD、
  pacman hooks 和 build receipt。
- Ubuntu `.deb` 不能作为 Arch package；可复用的是 source、patch、final config
  与硬件验证结论。
- `linux-uconsole` 至少提供 versioned image、modules、headers、DTBs 和
  uConsole overlays。
- config 采用“CM4 Lite 定向、常用外设通用”策略：可删除不可能使用的 PCIe
  独显和服务器设备，但必须保留 USB HID/storage/network/audio/webcam、
  Bluetooth、SCSI/UAS 和常用文件系统。

## Boot

PoC 使用 Raspberry Pi firmware direct boot 和 `config.txt`/DT overlays。
在专门审计完成前，不采用 Arch Linux ARM 默认的 U-Boot AArch64 启动链。

长期 boot updater 必须：

- 保持 `current` 与 `new` 两个 boot slot；
- 每个 slot 包含完整 Raspberry Pi firmware/overlay catalogue、kernel、
  initramfs、DTB 和 uConsole overlays；
- 新 kernel 只写 `new`，不得直接覆盖 known-good `current`；
- validator 在 promote 或标记失败前原子写入 FAT 诊断信箱；
- panel、backlight、rootfs、input、PMIC 或 DRM 健康检查失败时回退；
- 不依赖 UART 才能取得故障信息。

## Packages

计划中的原生 package：

- `linux-uconsole`
- `linux-uconsole-headers`
- `uconsole-kernel` meta-package
- `uconsole-platform`
- `uconsole-firstboot`
- `uconsole-desktop-sway`（可选）

package 通过签名 pacman repository 分发。repository release 使用 exact tag 和
不可变 bundle；promotion 复用完全相同的字节。

## Desktop

基础 image 先做到 console/SSH 和硬件完整可用。Sway 桌面是后续独立层，需求来源
为 `mew-console` 的 `codex/archlinux-arm` branch。

桌面层必须：

- 首次启动创建任意用户名；
- 使用 `$HOME` 与 XDG 路径；
- 锁定 Codex/npm package version 和 integrity；
- 不包含个人主题选择、登录状态或网络凭据；
- Tailscale 未认证，Shairport Sync 默认禁用。

## Release evidence

每个 release 绑定：

- rootfs archive/signature；
- source commit、config/patch hashes；
- compiler/makepkg/mkinitcpio versions；
- binary/source package set；
- signed pacman repo receipt；
- image SHA、SBOM 和 mounted validation；
- 同一字节的 CM4 Lite hardware report；
- 失败诊断和 rollback 结论。
