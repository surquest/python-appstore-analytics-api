import json
from surquest.utils.appstoreconnect.analytics.formatter import Formatter
from surquest.utils.appstoreconnect.analytics.enums import Measure, Group, Frequency
# load data from json file into a variable

data = {
    "grouped": json.load(open("../data/sample/input.grouped.json"))
} 


class TestFormatter:

    def test_run(self):

        out = Formatter.run(
            data=data.get("grouped"),
            grouping=Group.TOTAL,
            measure=Measure.INSTALLS
        )

        # # write out data into a json file
        # with open("../data/sample/output.formatted.json", "w") as f:
        #     json.dump(out, f, indent=4)

        assert isinstance(out, list), F"Expected type: list, got: {type(out)}."

        expected_keys = ["date", "app_id", "segmentation_name", "segment_", "__record_month", "__record_create_date"]

        for item in out:

            for key in expected_keys:

                assert key in item, F"Expected key: {key} to be in item: {item}."
