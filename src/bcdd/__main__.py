import sys
from typing import Optional
from bcdd import crypto, data, color, option

class Main:
    def __init__(self):
        self.print_file_names()
        cc = self.select_cc()
        if cc is None:
            self.exit()
        self.cc = cc
        self.cc_str = cc.replace("jp", "")
        self.run()
    
    def select_cc(self) -> Optional[str]:
        ccs = ["en", "jp", "kr", "tw"]
        cc_items = option.Item.name_list_to_item_list(ccs)
        cc_selector = option.ListSelector(cc_items, "Select a country code:")
        cc_index = cc_selector.get_index()
        if cc_index is None:
            return None
        return ccs[cc_index]

    def print_file_names(self):
        color.ColoredText().display(".dat file names:")
        file_names: dict[str, str] = {
            "Gatya data": "09b1058188348630d98a08e0f731f6bd.dat",
            "Daily reward data": "408f66def075926baea9466e70504a3b.dat",
            "Sale data": "002a4b18244f32d7833fd81bc833b97f.dat",
            "Ad control data": "523af537946b79c4f8369ed39ba78605.dat"
        }
        for name, file_name in file_names.items():
            color.ColoredText().display(f"  <green>{name}</>: {file_name}")

    def run(self):
        while True:
            try:
                self.first_menu()
            except KeyboardInterrupt:
                self.exit()
            
    def first_menu(self):
        items = [
            option.Item("Decrypt a .dat file", func=self.decrypt),
            option.Item("Encrypt a .dat file", func=self.encrypt),
            option.Item("Exit", func=self.exit)
        ]
        selector = option.ListSelector(items, "What do you want to do?")
        index = selector.get_index()
        if index is None:
            return
        items[index].run()
    
    def decrypt(self):
        file = option.FileSelector("Select a .dat file to decrypt", [("dat files", "dat"), ("All files", "*")]).get()
        if file is None:
            return
        file_name = file.get_file_name_without_extension()
        default_path = file.parent().add(file_name + "_decrypted.dat")
        output_file = option.FileSelector("Select an output file", [("dat files", "dat"), ("All files", "*")]).save(default_path)
        if output_file is None:
            return
        color.ColoredText().display(f"Decrypting <green>{file}</> to <green>{output_file}</>...")
        key = crypto.Hash(crypto.HashAlgorithm.MD5, data.Data("battlecats")).get_hash(16)
        aes_cipher = crypto.AesCipher(key.to_bytes())
        file_data = file.read()
        decrypted = aes_cipher.decrypt(file_data[:-32])

        output_file.write(decrypted)

    def encrypt(self):
        file = option.FileSelector("Select a .dat file to encrypt", [("dat files", "dat"), ("All files", "*")]).get()
        if file is None:
            return
        file_name = file.get_file_name_without_extension()
        default_path = file.parent().add(file_name + "_encrypted.dat")
        output_file = option.FileSelector("Select an output file", [("dat files", "dat"), ("All files", "*")]).save(default_path)
        if output_file is None:
            return
        color.ColoredText().display(f"Encrypting <green>{file}</> to <green>{output_file}</>...")
        key = crypto.Hash(crypto.HashAlgorithm.MD5, data.Data("battlecats")).get_hash(16)
        aes_cipher = crypto.AesCipher(key.to_bytes())
        encrypted = aes_cipher.encrypt(file.read())

        salt = data.Data(f"battlecats{self.cc_str}")

        file_hash = data.Data(crypto.Hash(crypto.HashAlgorithm.MD5, salt + encrypted).get_hash().to_hex())
        encrypted += file_hash

        output_file.write(encrypted)

    def exit(self):
        color.ColoredText().display("\n<green>Goodbye!</>")
        sys.exit()
    
if __name__ == "__main__":
    main = Main()
