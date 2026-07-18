# Infrastructure policy

本目录未来维护：

- boot/kernel A/B state machine；
- package repository/signing policy；
- artifact retention；
- release classification；
- rootfs update/rollback；
- CI action pinning；
- builder VM 资源与持久 cache 策略。

CI 只运行无特权静态检查。完整 kernel/package/image build 留在受控 ARM64 Linux
builder，不上传未经硬件验证的 release。
