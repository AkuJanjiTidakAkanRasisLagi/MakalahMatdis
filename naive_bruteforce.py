import time
from collections import defaultdict
from typing import List, Tuple, Set


class GroupAssigner:
    def __init__(self, n_students: int, task1_groups: List[Tuple[int, int, int]]):
        """
        :param n_students: Jumlah mahasiswa (harus kelipatan 3, mis. 18).
        :param task1_groups: Daftar tuple (s1, s2, s3) yang menunjukkan
                             mahasiswa s1, s2, s3 berada dalam 1 kelompok TB1.
        """
        self.n_students = n_students
        self.count = 0
        self.iterations = 0

        # forbidden_pairs[s] = set of mahasiswa yang TIDAK boleh sekelompok dengan s
        self.forbidden_pairs = defaultdict(set)
        for (s1, s2, s3) in task1_groups:
            self.forbidden_pairs[s1].update([s2, s3])
            self.forbidden_pairs[s2].update([s1, s3])
            self.forbidden_pairs[s3].update([s1, s2])

    def can_form_group(self, group: Tuple[int, int, int], used_students: Set[int]) -> bool:
        """
        Mengecek apakah 3 mahasiswa (group) bisa dibentuk:
        - Tidak ada yang sudah dipakai (used_students).
        - Tidak ada pair terlarang dalam group.
        """
        self.iterations += 1
        s1, s2, s3 = group

        # Pastikan belum dipakai
        if s1 in used_students or s2 in used_students or s3 in used_students:
            return False

        # Pastikan tidak ada forbidden pair
        if (s2 in self.forbidden_pairs[s1] or
            s3 in self.forbidden_pairs[s1] or
                s3 in self.forbidden_pairs[s2]):
            return False

        return True

    def backtrack(self,
                  used_students: Set[int],
                  current_groups: List[Tuple[int, int, int]]):
        """
        Backtracking untuk membentuk semua kemungkinan pembagian kelompok.
        - Jika semua mahasiswa sudah terpakai (len(used_students) == n_students), tambah self.count.
        - Jika belum, cari mahasiswa pertama yang belum dipakai, coba bentuk group bersamanya.
        """
        if len(used_students) == self.n_students:
            self.count += 1
            return

        # Cari mahasiswa pertama yang belum digunakan
        start_student = 0
        while start_student in used_students and start_student < self.n_students:
            start_student += 1

        # Coba bentuk group dengan start_student sebagai salah satu anggotanya
        for student2 in range(start_student + 1, self.n_students):
            if student2 in used_students:
                continue

            for student3 in range(student2 + 1, self.n_students):
                if student3 in used_students:
                    continue

                group = (start_student, student2, student3)
                if self.can_form_group(group, used_students):
                    # Pakai group ini
                    used_students.update([start_student, student2, student3])
                    current_groups.append(group)

                    # Lanjut backtrack
                    self.backtrack(used_students, current_groups)

                    # Kembalikan state (backtrack)
                    used_students.remove(start_student)
                    used_students.remove(student2)
                    used_students.remove(student3)
                    current_groups.pop()

    def count_possibilities(self):
        self.count = 0
        self.iterations = 0
        used_students = set()
        current_groups = []
        self.backtrack(used_students, current_groups)
        return self.count, self.iterations


class OptimizedGroupAssigner(GroupAssigner):
    """
    Optimized version: di dalam backtrack, kita menambahkan parameter start_student
    agar tidak selalu mulai dari 0 dan mempercepat pencarian.
    """

    def backtrack(self,
                  used_students: Set[int],
                  current_groups: List[Tuple[int, int, int]],
                  start_student: int = 0):
        if len(used_students) == self.n_students:
            self.count += 1
            return

        # Cari mahasiswa pertama yg belum terpakai, mulai dari start_student
        while start_student < self.n_students and (start_student in used_students):
            start_student += 1

        if start_student >= self.n_students:
            return

        # Coba bentuk group dengan start_student
        for student2 in range(start_student + 1, self.n_students):
            if student2 in used_students:
                continue

            for student3 in range(student2 + 1, self.n_students):
                if student3 in used_students:
                    continue

                group = (start_student, student2, student3)
                if self.can_form_group(group, used_students):
                    used_students.update([start_student, student2, student3])
                    current_groups.append(group)

                    # Lanjut backtrack dengan start_student + 1
                    self.backtrack(used_students, current_groups,
                                   start_student + 1)

                    # Kembalikan state
                    used_students.remove(start_student)
                    used_students.remove(student2)
                    used_students.remove(student3)
                    current_groups.pop()

        # Coba juga skip start_student sepenuhnya
        self.backtrack(used_students, current_groups, start_student + 1)


def test_both_versions(n_students: int):
    """
    Membuat task1_groups sederhana (setiap 3 mahasiswa = 1 kelompok TB1),
    lalu membandingkan kinerja versi original (GroupAssigner) dengan versi
    OptimizedGroupAssigner.
    """
    # Buat task1_groups (tiap 3 mahasiswa dijadikan satu kelompok TB1)
    task1_groups = []
    for i in range(0, n_students, 3):
        task1_groups.append((i, i+1, i+2))

    # Original version
    start_time = time.time()
    original = GroupAssigner(n_students, task1_groups)
    orig_possibilities, orig_iterations = original.count_possibilities()
    end_time = time.time()
    duration = end_time - start_time
    print(f"Possibilities: {orig_possibilities}")
    # print(f"Iterations: {orig_iterations}")
    print(f"Time: {duration*1000:.2f} ms")


if __name__ == "__main__":
    N = int(input("Enter the number of groups: "))  # Number of groups in TB1
    test_both_versions(3*N)
