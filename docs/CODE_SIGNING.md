# Podpis aplikace BleedMakr

## Proč podepisovat aplikace?

Podpis aplikace (Code Signing) je důležitý z několika důvodů:

### **🔒 Bezpečnost**
- **Windows Defender** - méně falešných poplachů
- **SmartScreen** - uživatelé vidí důvěryhodného vývojáře
- **Antivirus** - méně blokování aplikace

### **👤 Důvěryhodnost**
- Uživatelé vidí, kdo aplikaci vytvořil
- Profesionální vzhled
- Důvěra v bezpečnost aplikace

---

## **Možnosti podpisu**

### **1. Self-Signed Certificate (Zadarmo)**
```powershell
# Vytvoření certifikátu
$cert = New-SelfSignedCertificate -Subject "CN=BleedMakr, O=BleedMakr Team, C=CZ" -Type CodeSigningCert -CertStoreLocation "Cert:\CurrentUser\My"

# Podpis aplikace
Set-AuthenticodeSignature -FilePath "BleedMakr.exe" -Certificate $cert
```

**Výhody:**
- ✅ Zdarma
- ✅ Automatické v build procesu
- ✅ Méně agresivní varování

**Nevýhody:**
- ⚠️ Stále varování "Neznámý vydavatel"
- ⚠️ Uživatelé musí potvrdit spuštění

### **2. Code Signing Certificate (Placené)**
```powershell
# Použití komerčního certifikátu
$cert = Get-ChildItem -Path "Cert:\CurrentUser\My" | Where-Object {$_.Subject -like "*DigiCert*"}
Set-AuthenticodeSignature -FilePath "BleedMakr.exe" -Certificate $cert
```

**Výhody:**
- ✅ Žádná varování
- ✅ Plně důvěryhodný
- ✅ Profesionální vzhled

**Nevýhody:**
- ❌ ~$100-500/rok
- ❌ Složitější proces získání

### **3. Windows App Certification (Zadarmo)**
- Microsoft certifikace pro Windows Store
- Složitější proces
- Vyžaduje dodržení pravidel Microsoft

---

## **Implementace v projektu**

### **Automatický podpis v build procesu**

Build skript (`scripts/build_exe.py`) automaticky podepíše aplikaci:

```python
def sign_executable(exe_path):
    """Podepíše .exe soubor digitálním certifikátem"""
    # Vytvoření self-signed certifikátu
    # Podpis aplikace
    # Kontrola výsledku
```

### **GitHub Actions workflow**

Workflow automaticky podepíše buildy:

```yaml
- name: Sign Windows executable
  run: |
    # Vytvoření certifikátu
    # Podpis aplikace
    # Kontrola výsledku
```

---

## **Jak to funguje**

### **1. Vytvoření certifikátu**
```powershell
$cert = New-SelfSignedCertificate -Subject "CN=BleedMakr, O=BleedMakr Team, C=CZ" -Type CodeSigningCert -CertStoreLocation "Cert:\CurrentUser\My" -NotAfter (Get-Date).AddYears(3)
```

### **2. Podpis aplikace**
```powershell
$result = Set-AuthenticodeSignature -FilePath "BleedMakr.exe" -Certificate $cert
```

### **3. Kontrola podpisu**
```powershell
Get-AuthenticodeSignature "BleedMakr.exe"
```

---

## **Výsledky**

### **Před podpisem:**
- ❌ Windows Defender varování
- ❌ SmartScreen blokování
- ❌ "Neznámý vydavatel"

### **Po podpisu (Self-Signed):**
- ✅ Méně agresivní varování
- ✅ "BleedMakr Team" jako vydavatel
- ✅ Možnost přidat do důvěryhodných

### **Po podpisu (Komerční certifikát):**
- ✅ Žádná varování
- ✅ Plně důvěryhodný
- ✅ Profesionální vzhled

---

## **Doporučení**

### **Pro vývoj (aktuální stav):**
- ✅ Self-signed certifikát
- ✅ Automatický podpis v build procesu
- ✅ Dokumentace pro uživatele

### **Pro produkci:**
- 🔄 Komerční certifikát
- 🔄 Windows App Certification
- 🔄 Microsoft Store distribuce

---

## **Řešení problémů**

### **Chyba "Certifikační řetěz"**
- Normální u self-signed certifikátů
- Aplikace je funkční, jen s varováním

### **Chyba "Access Denied"**
- Spustit PowerShell jako Administrator
- Zkontrolovat Execution Policy

### **Chyba "Certificate not found"**
- Vytvořit nový certifikát
- Zkontrolovat certifikát v Cert Manager

---

## **Příkazy pro manuální podpis**

```powershell
# Vytvoření certifikátu
New-SelfSignedCertificate -Subject "CN=BleedMakr, O=BleedMakr Team, C=CZ" -Type CodeSigningCert -CertStoreLocation "Cert:\CurrentUser\My"

# Podpis aplikace
$cert = Get-ChildItem -Path "Cert:\CurrentUser\My" | Where-Object {$_.Subject -like "*BleedMakr*"}
Set-AuthenticodeSignature -FilePath "BleedMakr.exe" -Certificate $cert

# Kontrola podpisu
Get-AuthenticodeSignature "BleedMakr.exe"
```

---

## **Další kroky**

1. **Testování** - ověřit, že podpis funguje
2. **Dokumentace** - přidat do README informace o podpisu
3. **Uživatelská příručka** - vysvětlit uživatelům, co dělat s varováními
4. **Komerční certifikát** - zvážit pro budoucí verze 