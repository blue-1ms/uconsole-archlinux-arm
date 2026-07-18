# Validation

测试层次：

1. manifest、license、provenance 和 repository policy；
2. PKGBUILD/package identity、ownership、install/upgrade/remove；
3. kernel config、modules、vermagic、headers、DT merge 和 mkinitcpio；
4. boot A/B、overlay catalogue、firmware 和 FAT diagnostics；
5. 只读 mounted-image validation；
6. CM4 Lite 实机 hardware checklist 和故意损坏回退。

缓存命中不能跳过 package、repository、image 或 mounted validation。
