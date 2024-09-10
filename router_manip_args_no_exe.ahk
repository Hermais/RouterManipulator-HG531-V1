pythonPath := ;"C:\Users\gombi\AppData\Local\Programs\Python\Python312\python.exe" Use you own python file path
pyScriptPath := "D:\SoftwareProjectFiles\Python_Projects\router_manipulator_laptop\example_args_router_manip.py"

^+!1::
{
    arg := 1
    Run, %pythonPath% %pyScriptPath% %arg%

    return
    
}

^+!2::
{
    arg := 2
    Run, %pythonPath% %pyScriptPath% %arg%

    return
    
}

^+!5::
{
    arg := 5.5
    Run, %pythonPath% %pyScriptPath% %arg%

    return
    
}

^+!c::
{
    arg := "chk"
    Run, %pythonPath% %pyScriptPath% %arg%


    return
    
}


^+!0::
{
    arg := "full"
    Run, %pythonPath% %pyScriptPath% %arg%


    return
    
}


^+!r::
{
    arg := "res"
    Run, %pythonPath% %pyScriptPath% %arg%


    return
    
}

^+!w::
{
    arg := "r"
    Run, %pythonPath% %pyScriptPath% %arg%


    return
    
}

^+!d::
{
    arg := "dis"
    Run, %pythonPath% %pyScriptPath% %arg%


    return
    
}

^+!q::
{
    arg := "qchk"
    Run, %pythonPath% %pyScriptPath% %arg%


    return
    
}

^+!g::
{
    arg := "getit"
    Run, %pythonPath% %pyScriptPath% %arg%


    return
    
}



