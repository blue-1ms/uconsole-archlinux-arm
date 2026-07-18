# Manifests

这里将保存唯一活动 manifest 和不可变历史 manifest：

```text
active.yaml
releases/<release-id>.yaml
```

在以下输入全部取得 exact URL、version、signature 和 SHA 前，不创建占位
`active.yaml`：

- Arch Linux ARM AArch64 Raspberry Pi rootfs
- pacman database/package lock
- `rpi-linux` source commit 与 config/patch series
- Raspberry Pi firmware
- compiler、makepkg 和 mkinitcpio toolchain
- optional desktop/npm inputs

release ID 不等于发布资格。没有 package、mounted-image 和硬件 evidence 的
manifest 只能代表构建定义。
