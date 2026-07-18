# uConsole Arch Linux ARM

面向 ClockworkPi uConsole CM4 Lite 的可重复构建 Arch Linux ARM
镜像控制面。

> 当前状态：仓库骨架。尚未生成、发布或验证任何可刷写镜像，也尚未生成或
> 验证任何 Arch kernel package。当前暂停 Arch package/image 构建，先等待
> Ubuntu 控制面中的 CM4 Lite lean kernel 完成实机验证并冻结不可变 receipt。

本项目计划使用签名且固定完整性信息的 Arch Linux ARM AArch64 rootfs，
结合 [`blue-1ms/rpi-linux`](https://github.com/blue-1ms/rpi-linux) 中经过
uConsole 审计的 kernel source、patch 和 config，生成可在 microSD 上测试的
Arch Linux ARM 镜像。

## 目标

- v1 只支持 ClockworkPi uConsole、CM4 Lite、microSD 和 CM4 自带
  Wi-Fi/Bluetooth。
- 使用 Raspberry Pi firmware direct boot；在另行审计前不采用 Arch Linux
  ARM 默认 AArch64 U-Boot 路径。
- 以原生 Arch packages（`.pkg.tar.zst`）、`pacman` hooks 和 `mkinitcpio`
  管理 kernel、platform 和 initramfs。
- 保留完整的 uConsole panel、backlight、input、audio、PMIC/battery、
  Wi-Fi/Bluetooth 与常用 USB 外设支持。
- kernel 更新进入独立 `new` boot slot；失败时回到 known-good `current`。
- kernel 滚动策略固定为：最新 hardware-passed kernel 是 `current`，紧邻
  上一版是唯一 N-1 known-good fallback，N-2 通过 package manager 清理。
- 无屏幕时仍可从 FAT boot 分区读取不含隐私数据的诊断信箱。
- 默认镜像不包含密码、SSH key、Wi-Fi、Tailscale、npm、GitHub 或 Codex
  凭据。

## 非目标

- 当前阶段不支持 CM3、CM4S、CM5、eMMC、4G、AIC8800 或公共 stable 发布。
- 不把 CM4 Lite lean config 宣称为 CM5 或其他机型的通用 config；新机型先从
  full config 建立独立 profile，再经过 config 与实机审计。
- 不直接安装或解包 Ubuntu `.deb` 作为 Arch package。
- 在共享 kernel receipt 标记为 hardware-passed 前，不构建或发布 Arch kernel
  package。
- 不在镜像中固化个人用户名或 `/home/mew`。
- 不跟随浮动 kernel branch、rootfs `latest` URL 或未锁定的 npm package
  生成 release。
- 不在本仓库提交 rootfs、kernel binaries、pacman packages 或完整 SD image。

## 仓库职责

```text
manifests/       唯一构建输入、source commit、package 与 archive 完整性
kernel/          Arch kernel config/patch inventory；source 保留在 rpi-linux
packaging/       PKGBUILD、pacman hooks、mkinitcpio 和 platform packages
image/           rootfs/boot 分区组合与镜像导出策略
scripts/         构建、审计、验证和 release 入口
infra/           boot A/B、更新、retention 与签名 policy
tests/           静态、package、mounted-image 与硬件验证
profile-assets/  通用可选桌面模板；不得包含个人状态
docs/            中文维护文档和 release evidence
```

详细职责边界见 [`docs/architecture.md`](docs/architecture.md)，阶段计划见
[`docs/roadmap.md`](docs/roadmap.md)，共享 kernel 接入政策见
[`docs/kernel-lineage.md`](docs/kernel-lineage.md)。

## 相关仓库

| 仓库 | 职责 |
|---|---|
| [`blue-1ms/rpi-linux`](https://github.com/blue-1ms/rpi-linux) | 共用的 uConsole kernel source、patch/config lineage |
| [`blue-1ms/uconsole-ubuntu-lts`](https://github.com/blue-1ms/uconsole-ubuntu-lts) | Ubuntu 构建与硬件验证基线，不作为 Arch package 来源 |
| [`blue-1ms/mew-console`](https://github.com/blue-1ms/mew-console/tree/codex/archlinux-arm) | Arch Sway 桌面需求与 first-boot 原型来源 |
| `blue-1ms/uconsole-arch-repo` | 未来的不可变、签名 pacman release bundle；尚未创建 |

## 安全与发布原则

- Arch Linux ARM rootfs 必须验证官方签名，并在 manifest 固定 archive SHA。
- 原始 rootfs 内的默认账户和默认密码必须在 image validation 前删除或锁定。
- Tailscale 可以安装但不得包含 auth state；Shairport Sync 默认保持禁用。
- 每个构建输入变化都使用新的 release ID；已记录 SHA 的产物不得同名覆盖。
- public release 必须绑定 exact source commit、package hashes、签名、mounted
  validation 与同一字节的 CM4 Lite 实机报告。

## License

- 构建代码、配置、PKGBUILD 和测试：Apache License 2.0，见
  [`LICENSE`](LICENSE)。
- 项目文档：Creative Commons Attribution 4.0 International，见
  [`LICENSE-DOCUMENTATION`](LICENSE-DOCUMENTATION)。
- Linux kernel 及第三方组件继续遵循各自许可证；来源和归属见
  [`NOTICE`](NOTICE)。
