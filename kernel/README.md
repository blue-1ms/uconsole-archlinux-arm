# Kernel control

Kernel source 和完整 Git 历史保留在
[`blue-1ms/rpi-linux`](https://github.com/blue-1ms/rpi-linux)。

本目录未来只保存：

- Arch/CM4 Lite final base config 和精简 fragment；
- patch inventory 与 ordered series；
- config migration report；
- DT merge expectations；
- source/config/patch hashes。

不得复制 Linux source tree、编译对象或 binary packages 到本目录。

## Config policy

- v1 的 lean profile 只覆盖 CM4 Lite；必须保留 BCM2711、VC4/V3D/DSI、
  CWU50、OCP8178、AXP PMIC、MMC、Broadcom Wi-Fi/BT、audio、input、DT、
  initramfs/A-B 以及常用 USB 和文件系统支持。
- 可以关闭 AMDGPU、Radeon、Nouveau、InfiniBand、FireWire、服务器 RAID/HBA、
  Intel PCIe Wi-Fi/网卡和与 BCM2711 无关的平台驱动。
- 禁止使用 `localmodconfig` 生成 release config。每个 profile 必须由可审计
  fragment 合并，并保存 final config、delta、required-symbol result 和 SHA。
- CM5 或其他型号必须建立独立 profile；不得复用 CM4 Lite lean final config。
- 只有共享 kernel receipt 已完成 CM4 Lite hardware validation 后，本项目才
  能将它固定为 Arch package 输入。

当前不构建 Arch kernel package。6.12 recovery 已退出活动交付，只保留历史
provenance；后续更新使用最新 hardware-passed `current` 加唯一 N-1 fallback。
