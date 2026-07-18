# Kernel lineage 与更新政策

## 当前决定

本仓库当前只维护 Arch Linux ARM 控制面和文档，不构建 `linux-uconsole`
`.pkg.tar.zst`、pacman repository 或 image。

Arch kernel 工作等待 Ubuntu 控制面中的 CM4 Lite candidate.16 lean kernel
完成以下门槛：

1. kernel、modules、headers、DTB/DTBO、initramfs 和 package receipt 验证；
2. 在真实 CM4 Lite 上通过 `new` slot try boot；
3. panel、backlight、DRM、input、audio、PMIC、Wi-Fi/BT 和常用 USB 清单；
4. promote、重启、FAT 诊断信箱和受控故障回退；
5. 冻结 exact `rpi-linux` tag/commit、config/patch hashes 和不可变 receipt。

通过前不得在 Arch 仓库复制 candidate binary，也不得将其标记为 Arch package
输入。Ubuntu `.deb` 永远不能直接安装到 Arch rootfs。

## 可共享与不可共享的部分

可以跨发行版复用：

- `rpi-linux` exact source commit/tag；
- uConsole panel、backlight、audio、PMIC 和 V3D/VC4 patch lineage；
- CM4 Lite final config、lean fragment、config delta 和 required-symbol audit；
- DT merge expectations 和硬件验证结论。

必须由 Arch 独立实现和验证：

- `PKGBUILD`、`.pkg.tar.zst` 和 package ownership；
- pacman repository、signing 和 hooks；
- `mkinitcpio` modules/hooks 与生成的 initramfs；
- Raspberry Pi firmware direct-boot updater 和 A/B slot transaction；
- Arch firmware、Mesa、systemd、rootfs 和 mounted-image validation。

## CM4 Lite lean profile

CM4 Lite lean profile 采用显式 allow/deny 与 required-symbol policy，不使用
`localmodconfig`。`localmodconfig` 取决于构建机器当时加载的模块；在 VM 中会
错误裁掉 uConsole 板载硬件和未插入的 USB 外设，也不能产生稳定的 release
输入。

lean profile 可以删除 CM4 Lite 不可能使用的独显、服务器、InfiniBand、
FireWire、RAID/HBA、Intel PCIe network 和无关 SoC/platform drivers，但必须
保留：

- BCM2711/CM4、VC4/V3D/DSI、CWU50、OCP8178、AXP PMIC 和 MMC；
- Broadcom Wi-Fi/Bluetooth、audio、input、DT、initramfs 和 A/B 依赖；
- USB HID/gamepad/serial/storage/UAS/network/Wi-Fi/audio/mic/UVC；
- Bluetooth、NFS/CIFS、ext4/FAT/exFAT/NTFS。

CM5 和其他机型不能复用 CM4 Lite lean final config。每个新 target 先以对应
Raspberry Pi full config 完成 bring-up，再建立独立 audited lean fragment、
manifest、ABI/package version 和硬件报告。

## 滚动更新与 retention

更新状态固定为：

```text
latest hardware-passed kernel = current
immediately previous kernel   = N-1 known-good fallback
older kernel                  = N-2, remove through pacman
```

每个 upstream version 或同版本 ABI 更新都使用新的 kernel ABI、package version、
release ID、签名 bundle 和 immutable receipt。新 kernel 只进入 `new` slot；
验证通过后 promote，失败自动回到 `current`。禁止覆盖已发布字节、直接写
kernel image、手工清空 boot tree 或绕过 FAT 诊断。

6.12 recovery 不进入 Arch 活动 manifest、package set、repository 或 image。
它的 source commit、SHA、provenance 和历史验证可以保留为文档证据。

## Kernel EOL

upstream EOL 不会立即阻止 Arch userspace 安装 package，但意味着 kernel 不再
自动得到上游安全与稳定性维护。适用的 LTS/CVE 修复可以逐项 backport；不能把
另一个 LTS 分支的补丁流机械套用到已 EOL kernel。

短期可以将已验证的 EOL kernel 保留为 N-1 fallback。日常 `current` 应迁移到
仍受支持的 Raspberry Pi/upstream 基线，并重新执行 config migration、patch
审计、package、A/B 和完整硬件验证。
