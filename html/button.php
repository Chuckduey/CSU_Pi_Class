<html>
<head>
<meta name="viewport" content="width=device-width" />
<title>LED Control</title>
<?php
     $but1_color="green";
     $but2_color="green";
     $but3_color="grey";
     $state = isset($_GET['state']) && is_numeric($_GET['state']) ? strval($_GET['state']) : 0;
echo "State is = ",$state;
?>
<br>

</head>
        <body>
<header>
        <h1>Fun with Raspberry Pi Relay and LED</h1>
        <h2 style="text-align: center">
</header>
        Control:
        <?php
        # $setmode4 = exec("/usr/bin/mraa-gpio set 7 output");
        # $setmode22 = exec("/usr/bin/mraa-gpio set 22 output");
         $setmode4 = shell_exec("/usr/bin/gpio -g mode 4 out");
         $setmode26 = shell_exec("/usr/bin/gpio -g mode 22 out");
        if($state & 1){
                $gpio_on1 = exec("/usr/bin/gpio write 4 0");
                $but1_color="green";
                echo " Relay 1 is on , ";
        }
        else{
                $gpio_off1 = exec("/usr/bin/gpio write 4 1");
                $but1_color="red";
                echo " Relay 1 is off , ";
        }
        if($state & 2){
                $gpio_on2 = exec("/usr/bin/gpio write 22 0");
                echo " LED 2 is on ";
                $but2_color="green";
        }
        else{
                $gpio_off2 = exec("/usr/bin/gpio write 22 1");
                echo " LED 2 is off ";
                $but2_color="red";
        }
        if($state == 3){
                $but3_color="green";
                echo" , --All On-- ";
                }
        ?>
        <p>

                <input type="submit" style="background-color:red" onclick="location.href='/button.php/?state=0';" value="All OFF"/>
                <input type="submit" style="background-color:<?= $but1_color ?>" onclick="location.href='/button.php/?state=1';" value=" ON 1 "/>
                <input type="submit" style="background-color:<?= $but2_color ?>" onclick="location.href='/button.php/?state=2';" value=" ON  2 "/>
                <input type="submit" style="background-color:<?= $but3_color ?>" onclick="location.href='/button.php/?state=3';" value="All On ""/><br>
        </p>
        </body>
</html>
