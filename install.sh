echo "Installing ypkg..."
cp -v ypkg.py /usr/bin/ypkg
chmod -v 755 /usr/bin/ypkg
ypkg
mkdir -p /var/lib/yellowpkg
cp -vr pkgs /var/lib/yellowpkg
chmod -vR 777 /var/lib/yellowpkg
echo "Testing changes..."
ypkg info hello
