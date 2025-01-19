import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from accel_to_draw import AccelerationProcessor

# Your test data
test_data = [{'x': 276, 'y': -16152, 'z': 2796, 'timestamp': 40692}, {'x': 952, 'y': -15996, 'z': 2680, 'timestamp': 40796}, {'x': 676, 'y': -16056, 'z': 2704, 'timestamp': 40900}, {'x': 456, 'y': -16256, 'z': 2708, 'timestamp': 41004}, {'x': 308, 'y': -16228, 'z': 3332, 'timestamp': 41108}, {'x': 272, 'y': -16184, 'z': 2824, 'timestamp': 41212}, {'x': 536, 'y': -16036, 'z': 3052, 'timestamp': 41316}, {'x': 692, 'y': -15880, 'z': 3332, 'timestamp': 41420}, {'x': 212, 'y': -16244, 'z': 2980, 'timestamp': 41524}, {'x': 272, 'y': -15996, 'z': 3032, 'timestamp': 41628}, {'x': 220, 'y': -16340, 'z': 3204, 'timestamp': 41732}, {'x': 352, 'y': -16664, 'z': 3356, 'timestamp': 41836}, {'x': 976, 'y': -15740, 'z': 3080, 'timestamp': 41940}, {'x': 200, 'y': -16928, 'z': 2776, 'timestamp': 42044}, {'x': -220, 'y': -16956, 'z': 3724, 'timestamp': 42148}, {'x': 72, 'y': -16460, 'z': 2600, 'timestamp': 42252}, {'x': 584, 'y': -17596, 'z': 3692, 'timestamp': 42356}, {'x': -1, 'y': -1, 'z': -1, 'timestamp': 42459}, {'x': 1200, 'y': -17152, 'z': 2408, 'timestamp': 42562}, {'x': 1748, 'y': -16976, 'z': 3488, 'timestamp': 42666}, {'x': 2200, 'y': -16684, 'z': 3264, 'timestamp': 42770}, {'x': 1500, 'y': -15000, 'z': 940, 'timestamp': 42874}, {'x': -1, 'y': -1, 'z': -1, 'timestamp': 42977}, {'x': 932, 'y': -13464, 'z': -1956, 'timestamp': 43080}, {'x': 3136, 'y': -14692, 'z': -1076, 'timestamp': 43184}, {'x': 1484, 'y': -14876, 'z': -968, 'timestamp': 43288}, {'x': 1228, 'y': -15132, 'z': -684, 'timestamp': 43392}, {'x': 528, 'y': -14980, 'z': 732, 'timestamp': 43496}, {'x': -564, 'y': -15180, 'z': 1140, 'timestamp': 43600}, {'x': -1532, 'y': -16500, 'z': 2176, 'timestamp': 43704}, {'x': -1236, 'y': -16456, 'z': 2324, 'timestamp': 43808}, {'x': -1688, 'y': -17268, 'z': 3108, 'timestamp': 43912}, {'x': -2692, 'y': -17040, 'z': 2696, 'timestamp': 44016}, {'x': -2000, 'y': -17128, 'z': 3588, 'timestamp': 44120}, {'x': -516, 'y': -17124, 'z': 3228, 'timestamp': 44224}, {'x': -2736, 'y': -16308, 'z': 2800, 'timestamp': 44328}, {'x': -924, 'y': -16184, 'z': 4440, 'timestamp': 44432}, {'x': -48, 'y': -17160, 'z': 3524, 'timestamp': 44536}, {'x': -2792, 'y': -15932, 'z': 2804, 'timestamp': 44640}, {'x': -984, 'y': -16848, 'z': 2824, 'timestamp': 44744}, {'x': -2088, 'y': -15984, 'z': 4880, 'timestamp': 44848}, {'x': -628, 'y': -16404, 'z': 4740, 'timestamp': 44952}, {'x': -1060, 'y': -16684, 'z': 3852, 'timestamp': 45056}, {'x': -1384, 'y': -16420, 'z': 3628, 'timestamp': 45160}, {'x': -920, 'y': -16776, 'z': 3888, 'timestamp': 45264}, {'x': -68, 'y': -16196, 'z': 3264, 'timestamp': 45368}, {'x': -428, 'y': -16864, 'z': 3868, 'timestamp': 45472}, {'x': -612, 'y': -16960, 'z': 3904, 'timestamp': 45576}, {'x': 528, 'y': -16236, 'z': 3704, 'timestamp': 45680}, {'x': 736, 'y': -15876, 'z': 2616, 'timestamp': 45784}, {'x': -704, 'y': -16328, 'z': 2884, 'timestamp': 45888}, {'x': 1412, 'y': -17324, 'z': 4036, 'timestamp': 45992}, {'x': 1312, 'y': -16504, 'z': 4432, 'timestamp': 46096}, {'x': 1024, 'y': -15644, 'z': 1688, 'timestamp': 46200}, {'x': -1, 'y': -1, 'z': -1, 'timestamp': 46303}, {'x': 1212, 'y': -15156, 'z': 1108, 'timestamp': 46406}, {'x': 1256, 'y': -14424, 'z': 764, 'timestamp': 46510}, {'x': 552, 'y': -15236, 'z': 628, 'timestamp': 46614}, {'x': 948, 'y': -15012, 'z': 1628, 'timestamp': 46718}, {'x': -716, 'y': -14316, 'z': 64, 'timestamp': 46822}, {'x': -712, 'y': -15216, 'z': 3208, 'timestamp': 46926}, {'x': -2772, 'y': -17256, 'z': 1520, 'timestamp': 47030}, {'x': -1128, 'y': -15456, 'z': 3368, 'timestamp': 47134}, {'x': -1060, 'y': -16488, 'z': 5752, 'timestamp': 47238}, {'x': -2140, 'y': -17604, 'z': 3708, 'timestamp': 47342}, {'x': -1504, 'y': -16392, 'z': 5232, 'timestamp': 47446}, {'x': -2648, 'y': -17708, 'z': 3472, 'timestamp': 47550}, {'x': -1116, 'y': -17260, 'z': 3972, 'timestamp': 47654}, {'x': -2884, 'y': -17220, 'z': 6628, 'timestamp': 47758}, {'x': -2060, 'y': -16288, 'z': 3624, 'timestamp': 47862}, {'x': -1508, 'y': -15600, 'z': 2944, 'timestamp': 47966}, {'x': -444, 'y': -16612, 'z': 5592, 'timestamp': 48070}, {'x': -3104, 'y': -16676, 'z': 3952, 'timestamp': 48174}, {'x': -3008, 'y': -16428, 'z': 3976, 'timestamp': 48278}, {'x': -900, 'y': -17324, 'z': 3764, 'timestamp': 48382}, {'x': -1960, 'y': -17168, 'z': 3448, 'timestamp': 48486}, {'x': -808, 'y': -16712, 'z': 3996, 'timestamp': 48590}, {'x': 288, 'y': -16304, 'z': 4452, 'timestamp': 48694}, {'x': 136, 'y': -17372, 'z': 1424, 'timestamp': 48798}, {'x': 1268, 'y': -16376, 'z': 2996, 'timestamp': 48902}, {'x': 200, 'y': -16400, 'z': 3388, 'timestamp': 49006}, {'x': 276, 'y': -15240, 'z': 2056, 'timestamp': 49110}, {'x': 1512, 'y': -15396, 'z': 1984, 'timestamp': 49214}, {'x': -1, 'y': -1, 'z': -1, 'timestamp': 49317}, {'x': -1, 'y': -1, 'z': -1, 'timestamp': 49419}, {'x': -1, 'y': -1, 'z': -1, 'timestamp': 49521}, {'x': -1, 'y': -1, 'z': -1, 'timestamp': 49623}, {'x': -224, 'y': -13760, 'z': -460, 'timestamp': 49726}, {'x': -1392, 'y': -16016, 'z': 2284, 'timestamp': 49830}, {'x': -2240, 'y': -15828, 'z': 740, 'timestamp': 49934}, {'x': -2500, 'y': -16972, 'z': 1264, 'timestamp': 50038}, {'x': -2724, 'y': -17236, 'z': 4084, 'timestamp': 50142}, {'x': -2904, 'y': -16292, 'z': 3988, 'timestamp': 50246}, {'x': -2284, 'y': -16632, 'z': 3008, 'timestamp': 50350}, {'x': -1564, 'y': -16376, 'z': 2612, 'timestamp': 50454}, {'x': -2216, 'y': -17060, 'z': 2692, 'timestamp': 50558}, {'x': -304, 'y': -16660, 'z': 2328, 'timestamp': 50662}, {'x': -1252, 'y': -16604, 'z': 4000, 'timestamp': 50766}, {'x': 204, 'y': -16820, 'z': 3920, 'timestamp': 50870}, {'x': -1772, 'y': -16072, 'z': 3884, 'timestamp': 50974}, {'x': -56, 'y': -15424, 'z': 3956, 'timestamp': 51078}, {'x': 212, 'y': -16460, 'z': 5004, 'timestamp': 51182}, {'x': -548, 'y': -16316, 'z': 4684, 'timestamp': 51286}, {'x': -1400, 'y': -15880, 'z': 4436, 'timestamp': 51390}, {'x': -1240, 'y': -14896, 'z': 4076, 'timestamp': 51494}, {'x': -1832, 'y': -14996, 'z': 3984, 'timestamp': 51598}, {'x': -1160, 'y': -15932, 'z': 4180, 'timestamp': 51702}, {'x': -1316, 'y': -16500, 'z': 5484, 'timestamp': 51806}, {'x': -1516, 'y': -16436, 'z': 4716, 'timestamp': 51910}, {'x': -764, 'y': -15900, 'z': 5432, 'timestamp': 52014}, {'x': -1136, 'y': -15852, 'z': 5248, 'timestamp': 52118}, {'x': -1776, 'y': -16044, 'z': 4432, 'timestamp': 52222}, {'x': -1132, 'y': -15912, 'z': 5164, 'timestamp': 52326}, {'x': -1960, 'y': -15776, 'z': 4956, 'timestamp': 52430}, {'x': -1384, 'y': -15780, 'z': 4300, 'timestamp': 52534}, {'x': -1460, 'y': -15940, 'z': 4612, 'timestamp': 52638}]

def test_acceleration_processor():
    # Initialize the processor
    processor = AccelerationProcessor(window_size=10)
    
    # Lists to store positions for plotting
    positions_x = []
    positions_y = []
    positions_z = []
    
    # Process each data point
    for data_point in test_data:
        processor.add_point(
            x=data_point['x'],
            y=data_point['y'],
            z=data_point['z'],
            timestamp=data_point['timestamp']
        )
        
        # Store the position after each update
        x, y, z = processor.get_current_position()
        positions_x.append(x)
        positions_y.append(y)
        positions_z.append(z)
        
        # Print current position for debugging
        print(f"Timestamp: {data_point['timestamp']}, Position: ({x:.2f}, {y:.2f}, {z:.2f})")
    
    # Create 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the trajectory
    ax.plot(positions_x, positions_y, positions_z, 'b-', label='Trajectory')
    ax.scatter(positions_x, positions_y, positions_z, c='r', marker='o')
    
    # Set labels
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')
    ax.set_title('Acceleration to Position Trajectory')
    
    # Add legend
    ax.legend()
    
    # Show the plot
    plt.show()
    
    # Also create 2D plots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    
    # Plot X position over time
    ax1.plot(range(len(positions_x)), positions_x, 'r-')
    ax1.set_title('X Position over time')
    ax1.set_xlabel('Time steps')
    ax1.set_ylabel('X Position')
    
    # Plot Y position over time
    ax2.plot(range(len(positions_y)), positions_y, 'g-')
    ax2.set_title('Y Position over time')
    ax2.set_xlabel('Time steps')
    ax2.set_ylabel('Y Position')
    
    # Plot Z position over time
    ax3.plot(range(len(positions_z)), positions_z, 'b-')
    ax3.set_title('Z Position over time')
    ax3.set_xlabel('Time steps')
    ax3.set_ylabel('Z Position')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test_acceleration_processor()