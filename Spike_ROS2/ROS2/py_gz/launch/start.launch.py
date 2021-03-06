                                                        # you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Launches Gazebo and spawns a model
"""
import os
import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
             )

    # Get the full path to gazebo_motor_control

    gazebo_ros2_control_demos_path = os.path.join(
        get_package_share_directory('py_gz'))

    xacro_file = os.path.join(gazebo_ros2_control_demos_path,
                              'urdf',
                              'robot.xacro.urdf')

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)

    params = {'robot_description': doc.toxml()}
    print(params)

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
        arguments=['-entity', 'demo', '-topic', 'robot_description'],
        output='screen')


    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
    ])

