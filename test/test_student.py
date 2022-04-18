import student
from student import CSVStudentRepo


def test_get_student() -> None:
    csv_path = "../data/students_list.csv"

    with CSVStudentRepo(csv_path) as repo:
        assert repo.get_student("L201926630104").get_full_name() == "Chapata Tinashe"


def test_similar_group() -> None:
    """
    测试并查集
    """
    csv_path = "../data/students_list.csv"

    with CSVStudentRepo(csv_path) as repo:
        similar_group = student.SimilarGroup(repo)

    similar_group.union("L201926630114", "L201926630133")
    similar_group.union("L201926630126", "L201926630133")

    assert similar_group.find("L201926630114") == similar_group.find("L201926630126")
    assert not similar_group.find("L201926630134") == similar_group.find("L201926630133")
