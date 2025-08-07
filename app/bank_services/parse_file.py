import re
from datetime import datetime
from app.models.upload_file import CashWithdrawal

def parse_cash_withdrawals_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.findall(r"=+\s*CASH WITHDRAWAL\s*=+\n(.*?)=+", content, re.DOTALL)

    for block in blocks:
        try:
            lines = block.strip().split("\n")
            # 1: Sana va vaqt
            timestamp_str = lines[0].split(" - ")[0].strip()
            timestamp = datetime.strptime(timestamp_str, "%Y.%m.%d %H:%M:%S")

            # 2: PAN
            pan = lines[1].replace("PAN:", "").strip()

            # 3: AMOUNT
            amount_line = lines[2].replace("AMOUNT:", "").strip()
            amount_value = re.sub(r"[^\d.]", "", amount_line)  # faqat raqam va nuqta
            amount = float(amount_value)

            currency = "UZS"  # doimiy
            # 4: SOLUTION
            solution = lines[3].replace("SOLUTION:", "").strip()

            # Modelga yozamiz
            CashWithdrawal.objects.create(
                timestamp=timestamp,
                pan=pan,
                amount=amount,
                currency=currency,
                solution=solution
            )

        except Exception as e:
            print(f"Xatolik blokda: {block}\nXatolik: {e}")
