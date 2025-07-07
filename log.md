2025-07-06T15:46:56.6896262Z Current runner version: '2.325.0'
2025-07-06T15:46:56.6919423Z ##[group]Runner Image Provisioner
2025-07-06T15:46:56.6920161Z Hosted Compute Agent
2025-07-06T15:46:56.6920656Z Version: 20250703.357
2025-07-06T15:46:56.6921320Z Commit: 07daf62238a21140d93e045a38f3784d75c509e1
2025-07-06T15:46:56.6921909Z Build Date: 2025-07-03T14:39:09Z
2025-07-06T15:46:56.6922804Z ##[endgroup]
2025-07-06T15:46:56.6923466Z ##[group]Operating System
2025-07-06T15:46:56.6924220Z Microsoft Windows Server 2022
2025-07-06T15:46:56.6924787Z 10.0.20348
2025-07-06T15:46:56.6925184Z Datacenter
2025-07-06T15:46:56.6925587Z ##[endgroup]
2025-07-06T15:46:56.6925972Z ##[group]Runner Image
2025-07-06T15:46:56.6926510Z Image: windows-2022
2025-07-06T15:46:56.6927212Z Version: 20250623.1.0
2025-07-06T15:46:56.6928785Z Included Software: https://github.com/actions/runner-images/blob/win22/20250623.1/images/windows/Windows2022-Readme.md
2025-07-06T15:46:56.6931482Z Image Release: https://github.com/actions/runner-images/releases/tag/win22%2F20250623.1
2025-07-06T15:46:56.6932514Z ##[endgroup]
2025-07-06T15:46:56.6933575Z ##[group]GITHUB_TOKEN Permissions
2025-07-06T15:46:56.6935676Z Contents: read
2025-07-06T15:46:56.6936136Z Metadata: read
2025-07-06T15:46:56.6936598Z Packages: read
2025-07-06T15:46:56.6936992Z ##[endgroup]
2025-07-06T15:46:56.6939614Z Secret source: Actions
2025-07-06T15:46:56.6940350Z Prepare workflow directory
2025-07-06T15:46:56.7414187Z Prepare all required actions
2025-07-06T15:46:56.7468009Z Getting action download info
2025-07-06T15:46:56.9703495Z ##[group]Download immutable action package 'actions/checkout@v4'
2025-07-06T15:46:56.9704465Z Version: 4.2.2
2025-07-06T15:46:56.9705294Z Digest: sha256:ccb2698953eaebd21c7bf6268a94f9c26518a7e38e27e0b83c1fe1ad049819b1
2025-07-06T15:46:56.9706321Z Source commit SHA: 11bd71901bbe5b1630ceea73d27597364c9af683
2025-07-06T15:46:56.9706993Z ##[endgroup]
2025-07-06T15:46:57.0788820Z ##[group]Download immutable action package 'actions/setup-python@v4'
2025-07-06T15:46:57.0789590Z Version: 4.9.1
2025-07-06T15:46:57.0790243Z Digest: sha256:f03e505388af670b5a108629e0ba26befc08d5c62b41f46146a45fe29ae509a5
2025-07-06T15:46:57.0791118Z Source commit SHA: 7f4fc3e22c37d6ff65e88745f38bd3157c663f7c
2025-07-06T15:46:57.0791746Z ##[endgroup]
2025-07-06T15:46:57.3309290Z Download action repository 'actions/create-release@v1' (SHA:0cb9c9b65d5d1901c1f53e5e66eaf4afd303e70e)
2025-07-06T15:46:57.6123878Z Download action repository 'actions/upload-release-asset@v1' (SHA:e8f9f06c4b078e705bd2ea027f0926603fc9b4d5)
2025-07-06T15:46:57.9782951Z Complete job name: build-exe
2025-07-06T15:46:58.1192760Z ##[group]Run actions/checkout@v4
2025-07-06T15:46:58.1193926Z with:
2025-07-06T15:46:58.1194421Z   repository: h0nyik/BleedMakr
2025-07-06T15:46:58.1195265Z   token: ***
2025-07-06T15:46:58.1195750Z   ssh-strict: true
2025-07-06T15:46:58.1196252Z   ssh-user: git
2025-07-06T15:46:58.1196764Z   persist-credentials: true
2025-07-06T15:46:58.1197334Z   clean: true
2025-07-06T15:46:58.1197871Z   sparse-checkout-cone-mode: true
2025-07-06T15:46:58.1198514Z   fetch-depth: 1
2025-07-06T15:46:58.1199003Z   fetch-tags: false
2025-07-06T15:46:58.1199522Z   show-progress: true
2025-07-06T15:46:58.1200049Z   lfs: false
2025-07-06T15:46:58.1200517Z   submodules: false
2025-07-06T15:46:58.1201031Z   set-safe-directory: true
2025-07-06T15:46:58.1201840Z ##[endgroup]
2025-07-06T15:46:58.2811145Z Syncing repository: h0nyik/BleedMakr
2025-07-06T15:46:58.2813050Z ##[group]Getting Git version info
2025-07-06T15:46:58.2813831Z Working directory is 'D:\a\BleedMakr\BleedMakr'
2025-07-06T15:46:58.3966413Z [command]"C:\Program Files\Git\bin\git.exe" version
2025-07-06T15:46:58.6713316Z git version 2.50.0.windows.1
2025-07-06T15:46:58.6763406Z ##[endgroup]
2025-07-06T15:46:58.6784735Z Temporarily overriding HOME='D:\a\_temp\78f871b1-fac4-4e64-9346-e02e166d7982' before making global git config changes
2025-07-06T15:46:58.6789632Z Adding repository directory to the temporary git global config as a safe directory
2025-07-06T15:46:58.6802491Z [command]"C:\Program Files\Git\bin\git.exe" config --global --add safe.directory D:\a\BleedMakr\BleedMakr
2025-07-06T15:46:58.7250600Z Deleting the contents of 'D:\a\BleedMakr\BleedMakr'
2025-07-06T15:46:58.7258371Z ##[group]Initializing the repository
2025-07-06T15:46:58.7272016Z [command]"C:\Program Files\Git\bin\git.exe" init D:\a\BleedMakr\BleedMakr
2025-07-06T15:46:58.7859739Z Initialized empty Git repository in D:/a/BleedMakr/BleedMakr/.git/
2025-07-06T15:46:58.7898305Z [command]"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/h0nyik/BleedMakr
2025-07-06T15:46:58.8300162Z ##[endgroup]
2025-07-06T15:46:58.8301777Z ##[group]Disabling automatic garbage collection
2025-07-06T15:46:58.8308038Z [command]"C:\Program Files\Git\bin\git.exe" config --local gc.auto 0
2025-07-06T15:46:58.8535000Z ##[endgroup]
2025-07-06T15:46:58.8536607Z ##[group]Setting up auth
2025-07-06T15:46:58.8547502Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp core\.sshCommand
2025-07-06T15:46:58.8780106Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "sh -c \"git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :\""
2025-07-06T15:46:59.9636920Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2025-07-06T15:46:59.9858638Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "sh -c \"git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :\""
2025-07-06T15:47:00.4235217Z [command]"C:\Program Files\Git\bin\git.exe" config --local http.https://github.com/.extraheader "AUTHORIZATION: basic ***"
2025-07-06T15:47:00.4471028Z ##[endgroup]
2025-07-06T15:47:00.4472116Z ##[group]Fetching the repository
2025-07-06T15:47:00.4485577Z [command]"C:\Program Files\Git\bin\git.exe" -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +6fddc3849e10229cd7f1d18cac51bfaf8e3c381e:refs/tags/v0.0.1
2025-07-06T15:47:01.1899695Z From https://github.com/h0nyik/BleedMakr
2025-07-06T15:47:01.1900993Z  * [new ref]         6fddc3849e10229cd7f1d18cac51bfaf8e3c381e -> v0.0.1
2025-07-06T15:47:01.2126630Z ##[endgroup]
2025-07-06T15:47:01.2127268Z ##[group]Determining the checkout info
2025-07-06T15:47:01.2128774Z ##[endgroup]
2025-07-06T15:47:01.2142142Z [command]"C:\Program Files\Git\bin\git.exe" sparse-checkout disable
2025-07-06T15:47:01.2496671Z [command]"C:\Program Files\Git\bin\git.exe" config --local --unset-all extensions.worktreeConfig
2025-07-06T15:47:01.2715260Z ##[group]Checking out the ref
2025-07-06T15:47:01.2723619Z [command]"C:\Program Files\Git\bin\git.exe" checkout --progress --force refs/tags/v0.0.1
2025-07-06T15:47:01.3158294Z Note: switching to 'refs/tags/v0.0.1'.
2025-07-06T15:47:01.3158812Z 
2025-07-06T15:47:01.3159242Z You are in 'detached HEAD' state. You can look around, make experimental
2025-07-06T15:47:01.3159938Z changes and commit them, and you can discard any commits you make in this
2025-07-06T15:47:01.3160488Z state without impacting any branches by switching back to a branch.
2025-07-06T15:47:01.3160793Z 
2025-07-06T15:47:01.3160978Z If you want to create a new branch to retain commits you create, you may
2025-07-06T15:47:01.3161494Z do so (now or later) by using -c with the switch command. Example:
2025-07-06T15:47:01.3161766Z 
2025-07-06T15:47:01.3161992Z   git switch -c <new-branch-name>
2025-07-06T15:47:01.3162187Z 
2025-07-06T15:47:01.3162289Z Or undo this operation with:
2025-07-06T15:47:01.3162505Z 
2025-07-06T15:47:01.3162604Z   git switch -
2025-07-06T15:47:01.3162821Z 
2025-07-06T15:47:01.3163059Z Turn off this advice by setting config variable advice.detachedHead to false
2025-07-06T15:47:01.3163409Z 
2025-07-06T15:47:01.3163673Z HEAD is now at 6fddc38 Merge branch 'master' of https://github.com/h0nyik/BleedMakr
2025-07-06T15:47:01.3187037Z ##[endgroup]
2025-07-06T15:47:01.3472779Z [command]"C:\Program Files\Git\bin\git.exe" log -1 --format=%H
2025-07-06T15:47:01.3666284Z 6fddc3849e10229cd7f1d18cac51bfaf8e3c381e
2025-07-06T15:47:01.4026305Z ##[group]Run actions/setup-python@v4
2025-07-06T15:47:01.4026769Z with:
2025-07-06T15:47:01.4027233Z   python-version: 3.11
2025-07-06T15:47:01.4027647Z   check-latest: false
2025-07-06T15:47:01.4028072Z   token: ***
2025-07-06T15:47:01.4028285Z   update-environment: true
2025-07-06T15:47:01.4028583Z   allow-prereleases: false
2025-07-06T15:47:01.4028862Z ##[endgroup]
2025-07-06T15:47:01.6302542Z ##[group]Installed versions
2025-07-06T15:47:01.6566781Z Successfully set up CPython (3.11.9)
2025-07-06T15:47:01.6567499Z ##[endgroup]
2025-07-06T15:47:01.6814996Z ##[group]Run python -m pip install --upgrade pip
2025-07-06T15:47:01.6815425Z [36;1mpython -m pip install --upgrade pip[0m
2025-07-06T15:47:01.6815720Z [36;1mpip install -r requirements.txt[0m
2025-07-06T15:47:01.6815966Z [36;1mpip install pyinstaller[0m
2025-07-06T15:47:01.7122371Z shell: C:\Program Files\PowerShell\7\pwsh.EXE -command ". '{0}'"
2025-07-06T15:47:01.7122748Z env:
2025-07-06T15:47:01.7123032Z   pythonLocation: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:01.7123563Z   PKG_CONFIG_PATH: C:\hostedtoolcache\windows\Python\3.11.9\x64/lib/pkgconfig
2025-07-06T15:47:01.7124053Z   Python_ROOT_DIR: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:01.7124482Z   Python2_ROOT_DIR: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:01.7124905Z   Python3_ROOT_DIR: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:01.7125228Z ##[endgroup]
2025-07-06T15:47:09.4950414Z Requirement already satisfied: pip in c:\hostedtoolcache\windows\python\3.11.9\x64\lib\site-packages (25.1.1)
2025-07-06T15:47:11.1956235Z Collecting Pillow>=10.1.0 (from -r requirements.txt (line 1))
2025-07-06T15:47:11.2292072Z   Downloading pillow-11.3.0-cp311-cp311-win_amd64.whl.metadata (9.2 kB)
2025-07-06T15:47:11.4076267Z Collecting PyMuPDF>=1.23.0 (from -r requirements.txt (line 2))
2025-07-06T15:47:11.4139077Z   Downloading pymupdf-1.26.3-cp39-abi3-win_amd64.whl.metadata (3.4 kB)
2025-07-06T15:47:11.5540691Z Collecting reportlab>=4.0.0 (from -r requirements.txt (line 3))
2025-07-06T15:47:11.5589024Z   Downloading reportlab-4.4.2-py3-none-any.whl.metadata (1.8 kB)
2025-07-06T15:47:11.7708963Z Collecting numpy>=1.21.0 (from -r requirements.txt (line 4))
2025-07-06T15:47:11.7777421Z   Downloading numpy-2.3.1-cp311-cp311-win_amd64.whl.metadata (60 kB)
2025-07-06T15:47:11.8315229Z Collecting tkinterdnd2>=0.3.0 (from -r requirements.txt (line 5))
2025-07-06T15:47:11.8366822Z   Downloading tkinterdnd2-0.4.3-py3-none-any.whl.metadata (2.9 kB)
2025-07-06T15:47:11.9429008Z Collecting charset-normalizer (from reportlab>=4.0.0->-r requirements.txt (line 3))
2025-07-06T15:47:11.9489159Z   Downloading charset_normalizer-3.4.2-cp311-cp311-win_amd64.whl.metadata (36 kB)
2025-07-06T15:47:11.9766930Z Downloading pillow-11.3.0-cp311-cp311-win_amd64.whl (7.0 MB)
2025-07-06T15:47:12.0401595Z    ---------------------------------------- 7.0/7.0 MB 108.5 MB/s eta 0:00:00
2025-07-06T15:47:12.0502028Z Downloading pymupdf-1.26.3-cp39-abi3-win_amd64.whl (18.7 MB)
2025-07-06T15:47:12.2403950Z    ---------------------------------------- 18.7/18.7 MB 98.8 MB/s eta 0:00:00
2025-07-06T15:47:12.2514336Z Downloading reportlab-4.4.2-py3-none-any.whl (2.0 MB)
2025-07-06T15:47:12.2791104Z    ---------------------------------------- 2.0/2.0 MB 105.7 MB/s eta 0:00:00
2025-07-06T15:47:12.2872538Z Downloading numpy-2.3.1-cp311-cp311-win_amd64.whl (13.0 MB)
2025-07-06T15:47:12.3932289Z    ---------------------------------------- 13.0/13.0 MB 116.0 MB/s eta 0:00:00
2025-07-06T15:47:12.3987002Z Downloading tkinterdnd2-0.4.3-py3-none-any.whl (493 kB)
2025-07-06T15:47:12.4210517Z Downloading charset_normalizer-3.4.2-cp311-cp311-win_amd64.whl (105 kB)
2025-07-06T15:47:12.5529846Z Installing collected packages: tkinterdnd2, PyMuPDF, Pillow, numpy, charset-normalizer, reportlab
2025-07-06T15:47:20.4218500Z 
2025-07-06T15:47:20.4234403Z Successfully installed Pillow-11.3.0 PyMuPDF-1.26.3 charset-normalizer-3.4.2 numpy-2.3.1 reportlab-4.4.2 tkinterdnd2-0.4.3
2025-07-06T15:47:21.8593127Z Collecting pyinstaller
2025-07-06T15:47:21.8769542Z   Downloading pyinstaller-6.14.2-py3-none-win_amd64.whl.metadata (8.3 kB)
2025-07-06T15:47:21.8967931Z Requirement already satisfied: setuptools>=42.0.0 in c:\hostedtoolcache\windows\python\3.11.9\x64\lib\site-packages (from pyinstaller) (65.5.0)
2025-07-06T15:47:21.9216078Z Collecting altgraph (from pyinstaller)
2025-07-06T15:47:21.9262689Z   Downloading altgraph-0.17.4-py2.py3-none-any.whl.metadata (7.3 kB)
2025-07-06T15:47:21.9709088Z Collecting pefile!=2024.8.26,>=2022.5.30 (from pyinstaller)
2025-07-06T15:47:21.9754620Z   Downloading pefile-2023.2.7-py3-none-any.whl.metadata (1.4 kB)
2025-07-06T15:47:22.0181536Z Collecting pywin32-ctypes>=0.2.1 (from pyinstaller)
2025-07-06T15:47:22.0225167Z   Downloading pywin32_ctypes-0.2.3-py3-none-any.whl.metadata (3.9 kB)
2025-07-06T15:47:22.0772783Z Collecting pyinstaller-hooks-contrib>=2025.5 (from pyinstaller)
2025-07-06T15:47:22.0852754Z   Downloading pyinstaller_hooks_contrib-2025.5-py3-none-any.whl.metadata (16 kB)
2025-07-06T15:47:22.1586108Z Collecting packaging>=22.0 (from pyinstaller)
2025-07-06T15:47:22.1628890Z   Downloading packaging-25.0-py3-none-any.whl.metadata (3.3 kB)
2025-07-06T15:47:22.2038322Z Downloading pyinstaller-6.14.2-py3-none-win_amd64.whl (1.4 MB)
2025-07-06T15:47:22.2473631Z    ---------------------------------------- 1.4/1.4 MB 23.3 MB/s eta 0:00:00
2025-07-06T15:47:22.2515752Z Downloading packaging-25.0-py3-none-any.whl (66 kB)
2025-07-06T15:47:22.2811576Z Downloading pefile-2023.2.7-py3-none-any.whl (71 kB)
2025-07-06T15:47:22.3063811Z Downloading pyinstaller_hooks_contrib-2025.5-py3-none-any.whl (437 kB)
2025-07-06T15:47:22.3305874Z Downloading pywin32_ctypes-0.2.3-py3-none-any.whl (30 kB)
2025-07-06T15:47:22.3606471Z Downloading altgraph-0.17.4-py2.py3-none-any.whl (21 kB)
2025-07-06T15:47:22.4425260Z Installing collected packages: altgraph, pywin32-ctypes, pefile, packaging, pyinstaller-hooks-contrib, pyinstaller
2025-07-06T15:47:30.4844264Z 
2025-07-06T15:47:30.4859314Z Successfully installed altgraph-0.17.4 packaging-25.0 pefile-2023.2.7 pyinstaller-6.14.2 pyinstaller-hooks-contrib-2025.5 pywin32-ctypes-0.2.3
2025-07-06T15:47:31.1025381Z ##[group]Run Invoke-WebRequest -Uri "https://github.com/upx/upx/releases/download/v4.2.2/upx-4.2.2-win64.zip" -OutFile "upx.zip"
2025-07-06T15:47:31.1026270Z [36;1mInvoke-WebRequest -Uri "https://github.com/upx/upx/releases/download/v4.2.2/upx-4.2.2-win64.zip" -OutFile "upx.zip"[0m
2025-07-06T15:47:31.1026857Z [36;1mExpand-Archive -Path "upx.zip" -DestinationPath "."[0m
2025-07-06T15:47:31.1027192Z [36;1mMove-Item "upx-4.2.2-win64\upx.exe" "upx.exe"[0m
2025-07-06T15:47:31.1027576Z [36;1mecho "$PWD" | Out-File -FilePath $env:GITHUB_PATH -Encoding utf8 -Append[0m
2025-07-06T15:47:31.1058230Z shell: C:\Program Files\PowerShell\7\pwsh.EXE -command ". '{0}'"
2025-07-06T15:47:31.1058525Z env:
2025-07-06T15:47:31.1058753Z   pythonLocation: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:31.1059150Z   PKG_CONFIG_PATH: C:\hostedtoolcache\windows\Python\3.11.9\x64/lib/pkgconfig
2025-07-06T15:47:31.1059577Z   Python_ROOT_DIR: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:31.1059923Z   Python2_ROOT_DIR: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:31.1060268Z   Python3_ROOT_DIR: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:31.1060527Z ##[endgroup]
2025-07-06T15:47:32.8860500Z ##[group]Run python build_exe.py
2025-07-06T15:47:32.8860799Z [36;1mpython build_exe.py[0m
2025-07-06T15:47:32.8892069Z shell: C:\Program Files\PowerShell\7\pwsh.EXE -command ". '{0}'"
2025-07-06T15:47:32.8892366Z env:
2025-07-06T15:47:32.8892737Z   pythonLocation: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:32.8893139Z   PKG_CONFIG_PATH: C:\hostedtoolcache\windows\Python\3.11.9\x64/lib/pkgconfig
2025-07-06T15:47:32.8893514Z   Python_ROOT_DIR: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:32.8893854Z   Python2_ROOT_DIR: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:32.8894203Z   Python3_ROOT_DIR: C:\hostedtoolcache\windows\Python\3.11.9\x64
2025-07-06T15:47:32.8894517Z ##[endgroup]
2025-07-06T15:47:33.1534926Z Traceback (most recent call last):
2025-07-06T15:47:33.1541938Z   File "D:\a\BleedMakr\BleedMakr\build_exe.py", line 369, in <module>
2025-07-06T15:47:33.1542541Z     success = main()
2025-07-06T15:47:33.1542906Z               ^^^^^^
2025-07-06T15:47:33.1543386Z   File "D:\a\BleedMakr\BleedMakr\build_exe.py", line 336, in main
2025-07-06T15:47:33.1543977Z     print("\U0001f3a8 BleedMakr - Build .exe release")
2025-07-06T15:47:33.1544724Z   File "C:\hostedtoolcache\windows\Python\3.11.9\x64\Lib\encodings\cp1252.py", line 19, in encode
2025-07-06T15:47:33.1642201Z     return codecs.charmap_encode(input,self.errors,encoding_table)[0]
2025-07-06T15:47:33.1642868Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T15:47:33.1643757Z UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f3a8' in position 0: character maps to <undefined>
2025-07-06T15:47:33.2636215Z ##[error]Process completed with exit code 1.
2025-07-06T15:47:33.2825231Z Post job cleanup.
2025-07-06T15:47:33.5063235Z [command]"C:\Program Files\Git\bin\git.exe" version
2025-07-06T15:47:33.5285691Z git version 2.50.0.windows.1
2025-07-06T15:47:33.5377580Z Temporarily overriding HOME='D:\a\_temp\72043540-3a92-4e59-8ccd-3d8245443e5f' before making global git config changes
2025-07-06T15:47:33.5378666Z Adding repository directory to the temporary git global config as a safe directory
2025-07-06T15:47:33.5389802Z [command]"C:\Program Files\Git\bin\git.exe" config --global --add safe.directory D:\a\BleedMakr\BleedMakr
2025-07-06T15:47:33.5651556Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp core\.sshCommand
2025-07-06T15:47:33.5882780Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "sh -c \"git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :\""
2025-07-06T15:47:34.0638324Z [command]"C:\Program Files\Git\bin\git.exe" config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2025-07-06T15:47:34.0831756Z http.https://github.com/.extraheader
2025-07-06T15:47:34.0868566Z [command]"C:\Program Files\Git\bin\git.exe" config --local --unset-all http.https://github.com/.extraheader
2025-07-06T15:47:34.1099551Z [command]"C:\Program Files\Git\bin\git.exe" submodule foreach --recursive "sh -c \"git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :\""
2025-07-06T15:47:34.5446074Z Cleaning up orphan processes