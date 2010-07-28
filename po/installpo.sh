for file in *.po; do
locale=${file%.po}
sudo msgfmt $file -o /usr/share/locale/$locale/LC_MESSAGES/g15manager.mo
done
