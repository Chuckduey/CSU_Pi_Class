<html>
<head>
<meta name="viewport" content="width=device-width" />
<title>LED Control</title>
<?php
     $but1_color="green";
     $but2_color="green";
?>
</head>
        <body>
        LED Control:
        <form method="get" action="test2.php">
                <input style="background-color:<?php echo $but1_color; ?>" type="submit" value="ON 1" name="on1">
                <input type="submit" value="OFF 1" name="off1"><br>
                <input style="background-color:<?php echo $but2_color; ?> "type="submit" value="ON 2" name="on2">
                <input type="submit" value="OFF 2" name="off2"><br><br>

        </form>
        <?php
        $setmode25 = shell_exec("/usr/bin/gpio -g mode 25 out");
        $setmode26 = shell_exec("/usr/bin/gpio -g mode 26 out");
        if(isset($_GET['on1'])){
                $gpio_on1 = shell_exec("/usr/bin/gpio -g write 25 1");
                $but1_color="green";
                echo "LED 1 is on";
                echo "  Button Color = $but1_color";
        }
        else if(isset($_GET['off1'])){
                $gpio_off1 = shell_exec("/usr/bin/gpio -g write 25 0");
                $but1_color="red";
                echo "LED 1 is off. Button Color =";
                echo  "$but1_color";
        }
        if(isset($_GET['on2'])){
                $gpio_on2 = shell_exec("/usr/bin/gpio -g write 26 1");
                echo "LED 2 is on";
                $but2_color="green";
        }
        else if(isset($_GET['off2'])){
                $gpio_off2 = shell_exec("/usr/bin/gpio -g write 26 0");
                echo "LED 2 is off";
                $but2_color="red";
        }
        ?>
        </body>
</html>
