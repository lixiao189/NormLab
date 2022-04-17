from student import CSVStudentRepo


def test_get_student() -> None:
    csv_path = "../data/students_list.csv"

    with CSVStudentRepo(csv_path) as repo:
        assert repo.get_student("L201926630104").get_full_name() == "Chapata Tinashe"
