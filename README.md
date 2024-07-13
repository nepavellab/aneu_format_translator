<pre>
    <strong>
        FILE CONVERTATION
        _________________
  file                     file
+------+                 +------+
| .neu |       --->      |.aneu |
+------+                 +------+
    </strong>
</pre>

### **The start screen for selecting files** <br />
![main_display](https://github.com/user-attachments/assets/8fdcab6e-cd47-48c2-87d2-0b8d6a3f11bd) <br />

### **The process of processing a file and uploading it for viewing** <br />
![upload_display](https://github.com/user-attachments/assets/721f0ca9-7a0c-47aa-8ebf-fd3de35f03be) <br />

### **After processing and uploading files of both formats, you can view them (red shows the changes made by the algorithm)** <br />
![ready_display](https://github.com/user-attachments/assets/daedc8ef-f160-468f-b2a8-2b601ea47f30) <br />
![view_display](https://github.com/user-attachments/assets/ef9ccc6e-a90b-4ab4-ae0d-dd653727a0f1) <br />


### **Format mismatch error handling** <br />
![Снимок экрана (1210)](https://github.com/user-attachments/assets/0ee4feb4-5eb9-468f-9f82-a852dcf55fda) <br />

### The home screen object is described by the class:
```python
class MenuWidget(QWidget):
    # code
```

### The file display object is described by the class
```python
class ParseWidget(QWidget):
    # code
```

### Both presented objects are placed in the main window described by the class
```python
class MainWindow(QWidget):
    # code
```

### Windows settings for displaying the application icon
```python
myappid = u'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
```
