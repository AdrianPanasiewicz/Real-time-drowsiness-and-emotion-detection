from .parameter_finder import ParameterFinder
import numpy as np

class PerclosFinder(ParameterFinder):
    def __init__(self):
        self.left_eye_indices = [(385,380),(387,373),(263,362)]
        self.right_eye_indices = [(160,144),(158,153),(133,33)]
        self.ecr_per_face_memory = {1:{1:(0,0),2:(0,0)}} #TODO należy to podmienić po debugoawniu

    def find_parameter(self, face_coords):
        """
        #TODO Dokumentacja
        :param face_coords:
        :type face_coords:
        :return:
        :rtype:
        """
        left_ecr = self._find_eye_closure_ratio(face_coords, self.left_eye_indices)
        right_ecr = self._find_eye_closure_ratio(face_coords, self.right_eye_indices)
        perclos = self._calculate_perclos(left_ecr[0], right_ecr[0],1)

        return perclos

    @staticmethod
    def _find_eye_closure_ratio(face_coords, indices):
        """
        Metoda do obliczania szerokości otwarcia oczu
        #TODO Dokumentacja
        :param face_coords: Wynik działania modelu mediapipe
        :type face_coords:
        :param indices: Wartości indeksów dla landmarków oczu
        :type indices: list
        :return:
        :rtype:
        """
        all_delta_y = np.array([])
        all_faces_ecr = list()

        if face_coords.multi_face_landmarks:
            for face_mesh in face_coords.multi_face_landmarks:
                for pair in indices[0:-1]:
                    y2 = face_mesh.landmark[pair[0]].y
                    y1 = face_mesh.landmark[pair[1]].y

                    delta_y = abs(y2-y1)
                    all_delta_y = np.append(all_delta_y,delta_y)

                x2 = face_mesh.landmark[indices[-1][0]].x
                x1 = face_mesh.landmark[indices[-1][1]].x
                x_distance = abs(x2-x1)

                all_delta_y = np.array(all_delta_y)
                mean_y_distance = np.mean(all_delta_y)

                eye_closure_ratio = mean_y_distance / x_distance
                all_faces_ecr.append(eye_closure_ratio)

        return all_faces_ecr

    def _calculate_perclos(self, left_eye_closure_ratio, right_eye_closure_ratio, memory_key):
        """
        #TODO Dokumentacja
        :param left_eye_closure_ratio:
        :type left_eye_closure_ratio:
        :param right_eye_closure_ratio:
        :type right_eye_closure_ratio:
        :param memory_key:
        :type memory_key:
        :return:
        :rtype:
        """
        #TODO Automatyczne dodawanie osób
        #TODO Automatyczne usuwanie osób
        period = 60 #frames
        # Usuń najstarszą klatkę i dodaj obecną, jeśli okres jest dłuższy niż 10s
        if len(self.ecr_per_face_memory[memory_key])>=period:   #TODO Okres*FPS
            oldest_frame = min(self.ecr_per_face_memory[memory_key].keys())
            del self.ecr_per_face_memory[memory_key][oldest_frame]

        latest_frame = max(self.ecr_per_face_memory[memory_key].keys())
        ecr_ratios = (left_eye_closure_ratio, right_eye_closure_ratio)
        self.ecr_per_face_memory[memory_key].update({latest_frame + 1 : ecr_ratios})

        perclos = 0
        for _,pair in self.ecr_per_face_memory[memory_key].items():
            mean_from_pair = pair[0] + pair[1]
            if mean_from_pair < 0.3:
                perclos += 1

        perclos = perclos/period

        return perclos





