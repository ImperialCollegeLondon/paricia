# Permission system

Paricia's permissions system is designed to allow for data managers to add and validate new data, and the general public to view and retrieve the publicly released data. At the same time, it ensures data consistency by preventing submitted data to become orphan - eg. by accidental deletion of key information it depends on.

The following principles apply:

- **Anonymous users** (non-registered users) can view data in the reporting tool of stations that are labelled as **public**. These stations also appear in the map of the front page.
- **Registered users** can:
    - View data of stations owned by other users and labelled as **public** or **internal**, as well as their own data.
    - Create new elements, like formats, sensors, stations, etc. via the Admin interface. These elements can depend on other public objects or private objects owned by the user.
    - Upload new data to stations for which they have `change` permission (this includes stations they own).
    - Validate data associated to stations for which they have `change` permission (this includes stations they own).
- **Admin users** can:
    - Manage all data and objects, private or public.
    - Manage users.

!!! warning "Object deletion"

    Objects in the database **cannot be deleted if they are used by other objects**, regardless of the user permissions (even in the case of Admin users). For example, if a particular format uses certain delimiter, that delimiter object cannot be deleted. All associated objects need to be deleted first. See discussion [here](https://stackoverflow.com/a/48272690/3778792).

## Objects visibility

The **visibility** attribute of all objects in the database controls if the object can be viewed by anonymous users and referenced by other registered users in their own objects. When creating a new object, users must be careful to select a visibility level appropriate for their use case (public or private). If the object is public, then it can be referenced by objects of other users and therefore it will not be possible to delete it, should that be necessary at some point, since the owner of the object will not have access to the associated objects referencing their own.

**Stations** are a bit different to other objects in the following way:

   - To be able to reference them, a user must have `change` permission for that station. Making them public is not enough - that just makes their data publicly available.
   - They have another visibility level, `internal` which allows for the station data to be **visible to registered users only**.

The visibility of new objects always defaults to **private**.
