import win32com.client
import os
import pandas as pd
from . import helper

l = helper.GrabLogs()


def get_attch():
    fpath = f"{os.getcwd()}/comp_file"
    fpath = fpath.replace("/", "\\")
    fc = os.listdir(fpath)
    fc = sorted(fc)
    del fc[-1]
    return fc


def get_mail_details(map_file="mapping/HRBP_mailing_list.xlsx"):
    # sourcery skip: raise-specific-error
    try:
        if map_file is not None:
            return pd.read_excel(map_file, index_col=False)
    except:
        l.form_log("HRBP mailing list File is empty or cannot be found", 45)
        raise Exception("File not valid")


def match_lt_file():
    hrbp_df = get_mail_details()
    comp_list = get_attch()
    ord_list = []
    for ri, rcol in hrbp_df.iterrows():
        for idx in range(len(comp_list)):
            if rcol["LT"] in comp_list[idx]:
                ord_list.append(comp_list[idx])
            else:
                ord_list.append(f"To be solved for {rcol['LT']}")
                l.form_log(f"Can't be resolved for {rcol['LT']}", 20)
            break
    hrbp_df["Attach"] = ord_list
    return hrbp_df


def get_name(f_name):
    f_name = f_name.split(" ")
    return f_name[0]


# official mail function
def send_mail():
    raw_coord = match_lt_file()
    olmailitem = 0x0  # size of the new email
    for idx, val in raw_coord.iterrows():
        ol = win32com.client.Dispatch("outlook.application")
        newmail = ol.CreateItem(olmailitem)
        newmail.Subject = f'Comparisson File for {val["LT"]}'
        newmail.To = val["HRBP Mail"]
        newmail.CC = f'{val["HRD Mail"]}; {val["Tania Mail"]};{val["Florian Mail"]}'
        newmail.Body = (
            f"""Hello {get_name(val["HRBP"])}, \n Hope all is well! \n \nWe've started working on the quarterly KPIs, based on the last quarters' data. Would you mind validating the attached file, please, by this Friday EOB?"""
            + "\n \nCheers,\n\n"
        )
        if "To be solved for" in val["Attach"]:
            break
        else:
            attach = val["Attach"]
        newmail.Attachments.Add(attach)
        newmail.Display()


# for testing purposes
def send_dummy_mail(file_attach):
    ol = win32com.client.Dispatch("outlook.application")
    olmailitem = 0x0  # size of the new email
    newmail = ol.CreateItem(olmailitem)
    newmail.Subject = "Testing Mail"
    newmail.To = "vinod_boonratana@bat.com"
    newmail.CC = "florian_tatu@bat.com"
    newmail.Body = "Hello, this is a test email that contains an example of a json file. The file is harmless. Please do not reply."
    attach = file_attach
    newmail.Attachments.Add(attach)
    # To display the mail before sending it
    newmail.Display()
    # newmail.Send()


def chain_mail():
    base_chain = get_attch()
    for i in range(len(base_chain)):
        while i < 3:
            send_dummy_mail(base_chain[i])
            i += 1
        break
