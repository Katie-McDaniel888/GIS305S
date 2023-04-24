from GSheetsEtl import GSheetsEtl

if__name__=="main":
    etl_instance=GSheetEtl("https://foo_bar.com", "C:/Users", "GSheets", "C:Users/my.gdb")

    etl_instance.process()