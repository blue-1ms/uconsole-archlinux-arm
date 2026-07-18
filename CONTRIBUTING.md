# 贡献与维护约定

本仓库当前处于 Arch Linux ARM PoC 阶段。变更应保持小、可审计，并避免影响
已验证的 Ubuntu release。

## 基本规则

- `main` 承载下一次候选工作；release 使用不可变 tag，不维护长期 candidate
  branch。
- source、rootfs、package、toolchain 和 npm 输入必须固定 commit/version 与
  SHA-256 或签名证据。
- kernel source 留在 `blue-1ms/rpi-linux`；本仓库只保存 Arch config、patch
  inventory、PKGBUILD 和构建证据。
- 不提交 image、rootfs、package、cache、私钥、token、设备认证状态或任意
  `/home` 快照。
- 不直接写物理 SD 卡；image builder 只输出普通文件，刷卡属于单独的用户操作。
- 已记录 SHA 的失败产物不得同名重建；修复使用新的 release ID。

## 变更完成条件

实现构建接口后，每次提交至少运行：

```text
make docs-check
make validate
git diff --check
```

kernel、platform、image 或更新路径变化还必须执行对应 package/mounted-image
验证。只有 exact artifact bytes 完成 CM4 Lite 硬件清单后，才允许创建公开
release。

## License

提交代码即表示贡献按 Apache-2.0 提供；提交项目文档即表示贡献按 CC-BY-4.0
提供。第三方内容必须保留原始许可证、copyright 与 provenance。
