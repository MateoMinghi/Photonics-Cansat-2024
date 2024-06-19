# CanSat World Cup 2024

 <p align="center"><img src="https://github.com/MateoMinghi/Photonics/blob/main/img/banner_cansat.png"></p>

The CanSat World Course-Competition is an end-to-end life cycle complex engineering project challenge for students to incorporate the main subsystems found in a satellite (electronic components, sensors and a telemetry system).

The team[^1] participated in the 2024 edition, hosted by the National Autonomous University of Mexico (UNAM in spanish); and managed to reach the national finals.

For further information about the contest:
* http://peu.unam.mx/cansat2024.html
* https://www.cansatcompetition.com/

----
### Electronics System[^2]

The idea was to divide our satellite into two stages. The first stage only carried a GPS chip, while the second stage contained all the sensors (UV radiation, altitud, acceleration, pressure, GPS). 

Both stages had an independent LoRa module to transmit real-time information via radio to a third independent LoRa module, which was connected to the graphic interphase for the real-time data visualization.

Circuit for the primary stage:

<div align="center">
    <table>
        <tr>
            <td><b>Diagram</b></td>
            <td><b>Circuit</b></td>
        </tr>
        <tr>
            <td>
                <a href="https://github.com/MateoMinghi/Photonics/blob/main/img/primary_diagram.png">
                    <img src="https://github.com/MateoMinghi/Photonics/blob/main/img/primary_diagram.png" width="300" height="300">
                </img></a>
            </td>
            <td>
                <a href="https://github.com/MateoMinghi/Photonics/blob/main/img/primary_circuit.jpeg">
                    <img src="https://github.com/MateoMinghi/Photonics/blob/main/img/primary_circuit.jpeg" width="300" height="300">
                </img></a>
            </td>
        </tr>
    </table>
</div>


Circuit for the secondary stage:

<div align="center">
    <table>
        <tr>
            <td><b>Diagram</b></td>
            <td><b>Circuit</b></td>
        </tr>
        <tr>
            <td>
                <a href="https://github.com/MateoMinghi/Photonics/blob/main/img/secondary_diagram.png">
                    <img src="https://github.com/MateoMinghi/Photonics/blob/main/img/secondary_diagram.png" width="300" height="300">
                </img></a>
            </td>
            <td>
                <a href="https://github.com/MateoMinghi/Photonics/blob/main/img/secnodary_circuit.jpeg">
                    <img src="https://github.com/MateoMinghi/Photonics/blob/main/img/secnodary_circuit.jpeg" width="300" height="300">
                </img></a>
            </td>
        </tr>
    </table>
</div>



Project Design Slides:

* https://docs.google.com/file/d/1e1J56mg0GuxXB877cBg4IVVOmquFTbwD/edit?filetype=mspresentation

* https://docs.google.com/file/d/1e1J56mg0GuxXB877cBg4IVVOmquFTbwD/edit?filetype=mspresentation

* https://docs.google.com/presentation/d/1cosc5_qBbo0QIGDXYjj1O37L7R_xW0Vm/edit#slide=id.p1
 
---
### Data Visualization Interphase

In order to visualize the data retreived by the sensors, and transmited by the LoRa modules, it was decided to use Bokeh. Bokeh is an interactive visualization python library for web browsers. 

> Bokeh is particulary useful because it supports data streams,  allowing the plots to update automatically without having to refresh the browser, or even without having to save the data into a csv file.

The code can be foud inside the /Visualization/ folder.

To run the visualization, the dependencies found on requirements.txt must be installed, and using the following command:

```
bokeh serve --show main.py
```

Of course no data will be displayed unless the circuits are up and running, but a simulation of the interphase working can be found in /simulations.py

<p align="center"> <img src="https://github.com/MateoMinghi/Photonics/blob/main/img/visualization_cansat.jpg"/></p> 


[^1]: Team composed by: Mateo Minghi, Samir Baidon, Manuel Romero, Roberto Ibarra, Daniela Jimenez

[^2]: Electronics and Software designed and developed by Mateo Minghi, Samir Baidon, Daniela Jimenez 
