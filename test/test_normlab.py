from normlab import NormLab


def test_get_lab_id():
    lab = NormLab(
        "../data/Lab03-JUnit for Unit Test.zip"
    )

    assert lab.get_lab_id() == "Lab03"
