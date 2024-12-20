import numpy as np
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_LEFT_IRIS, FACEMESH_RIGHT_IRIS
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_LIPS, FACEMESH_LEFT_EYE, FACEMESH_RIGHT_EYE

from Workspace.Utilities import Utils


class CoordinatesParser:
    """
    Metoda do przetwarzania współrzędnych wskaźników na twarzy
    """

    def __init__(self):
        """Konstruktor klasy CoordinatesParser"""
        self._left_eye_indices = Utils.frozenset_to_list(FACEMESH_LEFT_EYE)
        self._right_eye_indices = Utils.frozenset_to_list(FACEMESH_RIGHT_EYE)
        self._mouth_indices = Utils.frozenset_to_list(FACEMESH_LIPS)
        self._left_iris_indices = Utils.frozenset_to_list(FACEMESH_LEFT_IRIS)
        self._right_iris_indices = Utils.frozenset_to_list(FACEMESH_RIGHT_IRIS)

    def find_left_eye(self, results) -> list:
        """
        Metoda do zawracania współrzędnych punktów orientacyjnych lewego oka.
        
        :param results: Wynik działania funkcji process od mediapipe
        :type results: Union
        :return: Lista z list bibliotek ze współrzędnymi punktów orientacyjnych lewego oka
        :rtype: list
        """

        all_left_eye_coords = list()
        if results.multi_face_landmarks:
            for face_mesh in results.multi_face_landmarks:
                left_eye_coords = list()
                for line in self._left_eye_indices:
                    line_coords = dict()
                    for number, index in enumerate(line, start=1):
                        line_coords.update({number: face_mesh.landmark[index]})
                    left_eye_coords.append(line_coords)

                all_left_eye_coords.append(left_eye_coords)

        return all_left_eye_coords

    def find_right_eye(self, results) -> list:
        """
        Metoda do zawracania współrzędnych punktów orientacyjnych prawego oka.

        :param results: Wynik działania funkcji process od mediapipe
        :type results: Union
        :return: Lista z list bibliotek ze współrzędnymi punktów orientacyjnych prawego oka
        :rtype: List
        """

        all_right_eye_coords = list()
        if results.multi_face_landmarks:
            for face_mesh in results.multi_face_landmarks:
                right_eye_coords = list()
                for line in self._right_eye_indices:
                    line_coords = dict()
                    for number, index in enumerate(line, start=1):
                        line_coords.update({number: face_mesh.landmark[index]})
                    right_eye_coords.append(line_coords)

                all_right_eye_coords.append(right_eye_coords)

        return all_right_eye_coords

    def find_mouth(self, results) -> list:
        """
        Metoda do zawracania współrzędnych punktów orientacyjnych ust.

        :param results: Wynik działania funkcji process od mediapipe
        :type results: Union
        :return: Lista z list bibliotek ze współrzędnymi punktów orientacyjnych ust
        :rtype: List
        """

        all_mouth_coords = list()
        if results.multi_face_landmarks:
            for face_mesh in results.multi_face_landmarks:
                mouth_coords = list()
                for line in self._mouth_indices:
                    line_coords = dict()
                    for number, index in enumerate(line, start=1):
                        line_coords.update({number: face_mesh.landmark[index]})
                    mouth_coords.append(line_coords)

                all_mouth_coords.append(mouth_coords)

        return all_mouth_coords

    @staticmethod
    def get_coordinates(face_elem_coords: list) -> tuple:
        """
        Metoda do uzyskania pozycji punktów w postaci trzech list dla osi x, y oraz z.

        :param face_elem_coords: Lista ze współrzędnymi x, y oraz z dla danego fragmentu twarzy
        :type face_elem_coords: list
        :return: Tuple wszystkich wymiarów
        :rtype: tuple
        """
        x_list_all = list()
        y_list_all = list()
        z_list_all = list()

        # Podzielenie listy face_elem_coord ze wszystkimi współrzędnymi na osobne listy.
        for face in face_elem_coords:
            x_list = list()
            y_list = list()
            z_list = list()

            for line in face:
                line_x = list()
                line_y = list()
                line_z = list()
                for key, value in line.items():
                    line_x.append(value.x)
                    line_y.append(1 - value.y)
                    line_z.append(value.z)

                x_list.append(line_x)
                y_list.append(line_y)
                z_list.append(line_z)

            x_list = np.array(x_list)
            y_list = np.array(y_list)
            z_list = np.array(z_list)

            x_list_all.append(x_list)
            y_list_all.append(y_list)
            z_list_all.append(z_list)

        return x_list_all, y_list_all, z_list_all

    def find_left_iris(self, results) -> list:
        """
        Metoda do zawracania współrzędnych punktów orientacyjnych lewej tęczówki.

        :param results: Wynik działania funkcji process od mediapipe
        :type results: Union
        :return: Lista z list bibliotek ze współrzędnymi punktów orientacyjnych lewej tęczówki
        :rtype: List
        """

        all_left_iris_coords = list()
        if results.multi_face_landmarks:
            for face_mesh in results.multi_face_landmarks:
                left_iris_coords = list()
                for line in self._left_iris_indices:
                    line_coords = dict()
                    for number, index in enumerate(line, start=1):
                        line_coords.update({number: face_mesh.landmark[index]})
                    left_iris_coords.append(line_coords)

                all_left_iris_coords.append(left_iris_coords)

        return all_left_iris_coords

    def find_right_iris(self, results) -> list:
        """
        Metoda do zawracania współrzędnych punktów orientacyjnych prawej tęczówki.

        :param results: Wynik działania funkcji process od mediapipe
        :type results: Union
        :return: Lista z list bibliotek ze współrzędnymi punktów orientacyjnych prawej tęczówki
        :rtype: List
        """

        all_right_iris_coords = list()
        if results.multi_face_landmarks:
            for face_mesh in results.multi_face_landmarks:
                left_iris_coords = list()
                for line in self._right_iris_indices:
                    line_coords = dict()
                    for number, index in enumerate(line, start=1):
                        line_coords.update({number: face_mesh.landmark[index]})
                    left_iris_coords.append(line_coords)

                all_right_iris_coords.append(left_iris_coords)

        return all_right_iris_coords
