# circuit-board
电路板铜线尺寸测量

* Install the libraries in the file `requirements.txt` with the script below:  
`pip3 install -r requirements.txt`

* Run the HTTP server with the script like this below:   
`python3 manage.py runserver 127.0.0.1:8000`

* Create a HTTP API request to get the response, ues POST request method, the image should be encoded by base64, 
that means it's a string format. Another parameter is shape in URL query parameters, it means one particular shape:    
`127.0.0.1:8000/measurement?shape=1`



```yaml
/measurement:
    post:
      parameters:
        - name: body
          in: body
          schema:
            properties:
              image:
                type: string
                description: 'image data(base64 encode)'
        - name: shape
          in: query
          required: true
          type: string
          description: 'one particular shape of the image'


      responses:
        200:
          description: OK
```