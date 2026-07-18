# Roadmap

## Phase 0：输入审计

- 固定并验证 Arch Linux ARM AArch64 Raspberry Pi rootfs。
- 审计 rootfs 分区/boot 预期、默认用户、pacman keyring 和 package set。
- 固定 `rpi-linux` commit、final config 与 mew-console requirements commit。
- 定义 manifest schema、release ID 和 artifact 命名。

完成条件：输入可重复下载和验证，不读取或携带敏感状态。

## Phase 1：最小启动

- 构建原生 `linux-uconsole` Arch package。
- 使用 Raspberry Pi firmware direct boot。
- 支持 CM4 Lite microSD、UART、SSH 和 FAT 诊断信箱。
- 不安装桌面。

完成条件：冷启动、热重启、rootfs mount、网络基础和诊断日志通过。

## Phase 2：完整硬件

- package 化 panel/backlight、audio routing、PMIC/battery、input 和 firmware。
- 验证新旧 CWU50 detection path、DRM、keyboard/game keys、trackball、
  speaker/headphone/mic、Wi-Fi/BT、USB 与关机。

完成条件：完整 CM4 Lite hardware checklist 通过。

## Phase 3：Kernel A/B 更新

- 实现 distro-neutral boot updater、`current`/`new` slot 和 pacman hooks。
- 建立签名 kernel-only pacman bundle。
- 验证安装、升级、旧 ABI 共存、故意损坏 `new` 自动回退和 FAT 分 slot 日志。

完成条件：失败不会破坏 known-good kernel 或使诊断只能依赖 UART。

## Phase 4：Sway 与 first boot

- 审计并迁移 `mew-console` Arch package list、greetd/Sway 和用户模板。
- 移除固定用户名，锁定 npm/Codex 输入。
- Shairport 保持 disabled，Tailscale 不带 auth state。

完成条件：任意用户名、首次登录、桌面硬件、profile 幂等与 rollback 通过。

## Phase 5：Test image

- 生成普通 image file、checksums、开发签名、SBOM 和 validation report。
- 只读 mounted-image validation 检查 package、boot、firmware、默认账户、
  无凭据和诊断服务。
- 同一个压缩 image 完成实机清单。

完成条件：只标记为 test image；public candidate 需另行完成 signing 和
reproducibility review。
