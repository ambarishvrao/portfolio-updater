from decimal import Decimal

import pytest

from casparser.exceptions import CASParseError, HeaderParseError
from casparser.process import process_cas_text
from casparser.process.cas_detailed import parse_header, get_transaction_type
from casparser.process.cas_detailed import ParsedTransaction, parse_transaction
from casparser.process.cas_summary import parse_header as parse_summary_header
from casparser.process.utils import isin_search
from casparser.enums import TransactionType


class TestProcessClass:
    def test_detailed_header_parser(self):
        good_header = "Consolidated Account Statement\n01-Apr-2018 To 31-Mar-2019"
        bad_header = "Consolidated Account Statement\n01-Apr-2018"

        header_data = parse_header(good_header)
        assert header_data == {"from": "01-Apr-2018", "to": "31-Mar-2019"}

        with pytest.raises(HeaderParseError):
            parse_header(bad_header)

    def test_summary_header_parser(self):
        good_header = "Consolidated Account Summary\nAs On 01-Apr-2018"
        bad_header = "Consolidated Account Summary\n01-Apr-2018"

        header_data = parse_summary_header(good_header)
        assert header_data == {"date": "01-Apr-2018"}

        with pytest.raises(HeaderParseError):
            parse_summary_header(bad_header)

    def test_process_bad_cas(self):
        with pytest.raises(CASParseError):
            process_cas_text("")

    def test_transaction_type(self):
        assert get_transaction_type("Redemption", Decimal(-100.0)) == (
            TransactionType.REDEMPTION,
            None,
        )
        assert get_transaction_type("Address updated", None) == (TransactionType.MISC, None)
        assert get_transaction_type("***STT paid ***", None) == (TransactionType.STT_TAX, None)
        assert get_transaction_type("***stamp duty***", None) == (
            TransactionType.STAMP_DUTY_TAX,
            None,
        )
        assert get_transaction_type("*** TDS on Above ***", None) == (TransactionType.TDS_TAX, None)
        assert get_transaction_type("Creation of units - Segregated portfolio", Decimal(1.0)) == (
            TransactionType.SEGREGATION,
            None,
        )
        assert get_transaction_type("***Random text***", Decimal(0.0)) == (
            TransactionType.UNKNOWN,
            None,
        )

        assert get_transaction_type(
            "Purchase SIPCheque Dishonoured - Instalment No 108", Decimal(-1.0)
        ) == (TransactionType.REVERSAL, None)

        assert parse_transaction(
            "01-Jan-2021\t\tCreation of units - Segregated Portfolio\t\t1.000\t\t12,601.184"
        ) == ParsedTransaction(
            date="01-Jan-2021",
            description="Creation of units - Segregated Portfolio",
            units="1.000",
            balance="12,601.184",
            nav=None,
            amount=None,
        )

    def test_dividend_transactions(self):
        assert get_transaction_type("IDCW Reinvestment @ Rs.2.00 per unit", Decimal(1.0)) == (
            TransactionType.DIVIDEND_REINVEST,
            Decimal("2.00"),
        )
        assert get_transaction_type("IDCW Reinvested @ Rs.0.0241 per unit", Decimal(1.0)) == (
            TransactionType.DIVIDEND_REINVEST,
            Decimal("0.0241"),
        )
        assert get_transaction_type("IDCW Paid @ Rs.0.06 per unit", Decimal(1.0)) == (
            TransactionType.DIVIDEND_PAYOUT,
            Decimal("0.06"),
        )
        # assert get_transaction_type("***IDCW Payout***", None) == (
        #     TransactionType.DIVIDEND_PAYOUT,
        #     None,
        # )
        assert get_transaction_type("Div. Reinvested @ Rs.0.0241 per unit", Decimal(1.0)) == (
            TransactionType.DIVIDEND_REINVEST,
            Decimal("0.0241"),
        )

    def test_isin_search(self):
        isin, amfi, scheme_type = isin_search(
            "Axis Long Term Equity Fund - Direct Growth", "KFINTECH", "128TSDGG"
        )
        assert isin == "INF846K01EW2"
        assert amfi == "120503"
        assert scheme_type == "EQUITY"

        isin, amfi, scheme_type = isin_search("", "KARVY", "")
        assert isin is None
        assert amfi is None
        assert scheme_type is None
