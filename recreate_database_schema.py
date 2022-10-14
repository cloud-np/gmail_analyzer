from extract_info import Extractor

if __name__ == "__main__":
    ext = Extractor()
    ext.uc.create_users_table()
    ext.mc.create_messages_table()
    ext.cc.create_proposed_ceremonies_table()