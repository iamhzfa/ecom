
# views.py

    # def post(self, request):
    #     user = request.user
    #     try:
    #         customerContact = CustomerContact.objects.get(user=request.user) 
    #         return Response({'error':'you have previously added your contact info'})
    #     except:   
    #         if not request.user.is_active:
    #             return Response("Your account is not active")
    #         data = request.data
    #         try:
    #             contact = data['contact']
    #         except:
    #             return Response({'contact':'this is required field'})

    #         serializer = CustomerContactSerializer(data=data, context={'user':user})
    #         serializer.is_valid(raise_exception=False)
    #         serializer.create(validated_data=serializer.data)
    #         return Response({'data':serializer.data})
    
    # def put(self, request, format=None):
        # try:
        #     customerContact = CustomerContact.objects.get(user=request.user) 
        # except:
        #     return Response({'error':'you have not provided any contact details yet'})
        # serializer = CustomerContactSerializer(customerContact,
        #                                    data=request.data)
                        
    #     serializer.is_valid(raise_exception=False)
    #     serializer.update(instance=customerContact, validated_data=serializer.data)
    #     return Response(serializer.data)


    # -----------------------------------------

# serializers.py

# def create(self, validated_data):
    #     user=self.context.get('user')
    #     user = CustomerContact.objects.create(user=user, **validated_data)
    #     return user
    # def update(self, instance, validated_data):
    #     for i in validated_data:
    #         if i=='contact':
    #             instance.contact = validated_data[i]
    #         if i=='alt_contact':
    #             instance.alt_contact = validated_data[i]
            
    #     instance.save()
    #     return instance 