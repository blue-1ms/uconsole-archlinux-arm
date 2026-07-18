# Security policy

## Supported status

本项目尚处于 PoC 阶段，没有 stable 或受支持的公开 image。

## Reporting

请通过 GitHub 的私密漏洞报告功能报告安全问题。不要在 public issue 中粘贴
密码、SSH key、Wi-Fi 配置、Tailscale state、npm/GitHub/Codex token、设备日志
中的个人信息或 signing private key。

## Image requirements

任何未来的 test image 都必须：

- 移除或锁定 Arch Linux ARM rootfs 中的默认账户和默认密码；
- 不包含 host SSH keys、machine-id、shell history 或用户 home snapshot；
- 不自动认证 Tailscale、GitHub、npm 或 Codex；
- 在显式配置前禁用 Shairport Sync 网络广播；
- 只向 FAT 诊断信箱写入经过 allowlist 的启动和硬件信息；
- 验证 rootfs、package repository 和 release checksum/signature。
