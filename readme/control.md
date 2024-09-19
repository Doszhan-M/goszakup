## Управление tender_pw:
```
systemctl --user restart tender_pw
systemctl --user start tender_pw
systemctl --user stop tender_pw
systemctl --user enable tender_pw
systemctl --user status tender_pw
journalctl --user -u tender_pw -f 
```

## Управление signer:
```
systemctl --user restart signer
systemctl --user start signer
systemctl --user stop signer
systemctl --user enable signer
systemctl --user status signer
journalctl --user -u signer -f
```
