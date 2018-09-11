<html>
<head>
<meta name="viewport" content="width=device-width" />
<title>LED Control</title>
<?php
     $but1_color="green";
     $but2_color="green";
?>
<script>
function setColor(btn, color){
    var count=1;
    var property = document.getElementById(btn);
    if (count == 0){
        property.style.backgroundColor = "#FFFFFF"
        count=1;        
    }
    else{
        property.style.backgroundColor = "#7FFF00"
        count=0;
    }

}
</script>

</head>
        <body>
<header>
        <h1>Fun with Raspberry Pi LEDs</h1>
        <h2 style="text-align: center">
</header>
        LED Control:
        <form method="get" action="test2.php">
                <input style="background-color:<?php echo $but1_color; ?>" type="submit" value="ON 1" name="on1">
                <input style="background-color:red" type="submit" value="OFF 1" name="off1"><br>
                <input style="background-color:<?php echo $but2_color; ?>" type="submit" value="ON 2" name="on2">
                <input style="background-color:red" type="submit" value="OFF 2" name="off2"><br><br>
        </form>
        <?php
        $setmode25 = shell_exec("/usr/bin/gpio -g mode 25 out");
        $setmode26 = shell_exec("/usr/bin/gpio -g mode 26 out");
        if(isset($_GET['on1'])){
                $gpio_on1 = shell_exec("/usr/bin/gpio -g write 25 1");
                $but1_color="green";
                echo "LED 1 is on";
        }
        else if(isset($_GET['off1'])){
                $gpio_off1 = shell_exec("/usr/bin/gpio -g write 25 0");
                $but1_color="red";
                echo "LED 1 is off";
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
