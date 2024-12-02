from Workspace import *
import matplotlib.pyplot as plt
from Workspace.Back_End.Data_Processing.Parameter_Finder import jawn_finder
from Workspace.Back_End.Data_Processing.Parameter_Finder import face_angle_finder

if __name__ == "__main__":

    pathlib.PosixPath = Utils.fix_pathlib()

    # Załadowanie klasy ImageProcessor do przetwarzania obrazu
    image_processor = ImageProcessor()
    crop_size = (224,224)
    text_color = [240, 10, 10]
    text_parameters = (cv2.FONT_HERSHEY_DUPLEX,1,text_color,2)

    # model_loader = ModelLoader()
    # models = model_loader.load_models()

    parameter_calculator = CoordinatesParser()
    face_plotter = face_plotter.FacePlotter()
    os.system('cls')

    # Initialise camera for video capture
    try:
        camera = cv2.VideoCapture(0)
        if camera is None or not camera.isOpened():
            raise TypeError

    except TypeError as e:
        raise TypeError('Nie udało się uzyskać dostępu do kamery lub kamera nie istnieje') from e

    past_tick = 0

    perclos_threshold = 0.4
    yawn_threshold = 0.6

    find_perclos = perclos_finder.PerclosFinder(perclos_threshold)
    find_jawn = jawn_finder.JawnFinder(yawn_threshold)
    find_face_tilt = face_angle_finder.FaceAngleFinder()
    find_saccade_velocity = saccade_speed_velocity.SaccadeVelocityFinder()
    saccs = np.zeros(1)
    while True:
        fps = Utils.calculate_fps()

        ret, frame = camera.read()
        # processed_frame_MM = image_processor.preprocess_image1(frame, *crop_size)
        processed_frame, face_mesh_coords = image_processor.preprocess_image2(frame)

        perclos = find_perclos.find_parameter(face_mesh_coords)
        is_jawning, jawn_counter = find_jawn.find_parameter(face_mesh_coords)
        head_tilt = find_face_tilt.find_parameter(face_mesh_coords)
        saccade_velocity = find_saccade_velocity.find_parameter(face_mesh_coords)

        # os.system('cls')
        # print(f"PERCLOS =\t{round(perclos,2)}")

        coords_left_eye = parameter_calculator.find_left_eye(face_mesh_coords)
        coords_right_eye = parameter_calculator.find_right_eye(face_mesh_coords)
        coords_mouth = parameter_calculator.find_mouth(face_mesh_coords)
        coords_left_iris = parameter_calculator.find_left_iris(face_mesh_coords)
        coords_right_iris = parameter_calculator.find_right_iris(face_mesh_coords)

        x_list_1, y_list_1, z_list_1 = parameter_calculator.get_coordinates(coords_left_eye)
        x_list_2, y_list_2, z_list_2 = parameter_calculator.get_coordinates(coords_right_eye)
        x_list_3, y_list_3, z_list_3 = parameter_calculator.get_coordinates(coords_mouth)
        x_list_4, y_list_4, z_list_4 = parameter_calculator.get_coordinates(coords_left_iris)
        x_list_5, y_list_5, z_list_5 = parameter_calculator.get_coordinates(coords_right_iris)

        face_plotter.update_xyz_coords(x_list_1,y_list_1,z_list_1,"LEFT_EYE")
        face_plotter.update_xyz_coords(x_list_2, y_list_2, z_list_2, "RIGHT_EYE")
        face_plotter.update_xyz_coords(x_list_3, y_list_3, z_list_3, "MOUTH")
        face_plotter.update_xyz_coords(x_list_4, y_list_4, z_list_4, "LEFT_IRIS")
        face_plotter.update_xyz_coords(x_list_5, y_list_5, z_list_5, "RIGHT_IRIS")

        # output = models["Emotion_model"].predict(processed_frame_MM)
        cv2.putText(processed_frame, f"Emotion: (Deactivated)", (15, 30), *text_parameters)
        cv2.putText(processed_frame, f"Saccade speed: {round(saccade_velocity, 3)}", (15, 60), *text_parameters)
        cv2.putText(processed_frame, f"PERCLOS: {int(perclos*100)}%", (15, 90), *text_parameters)
        cv2.putText(processed_frame, f"Jawn: {is_jawning}", (15, 120), *text_parameters)
        cv2.putText(processed_frame, f"Jawn counter: {jawn_counter}", (15, 150), *text_parameters)
        cv2.putText(processed_frame, f"Head tilt: {round(head_tilt, 2)}", (15, 180), *text_parameters)
        cv2.putText(processed_frame, f"FPS: {int(fps)}", (15, 210), *text_parameters)
        cv2.imshow('Drowsiness detection', processed_frame)
        stop_tick = time.process_time()

        # if len(saccs) >= 20:
        #     saccs = np.roll(saccs, -1)
        #     saccs[-1] = saccade_velocity
        # else:
        #     saccs = np.append(saccs, saccade_velocity)
        #
        # plt.axis([0, 20, -30, 0])
        # plt.plot(saccs)
        # plt.pause(0.001)
        # plt.clf()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()



