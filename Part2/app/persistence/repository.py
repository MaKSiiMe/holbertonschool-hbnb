from abc import ABC, abstractmethod

class Repository(ABC):
    """Abstract class for a generic repository."""
    
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass


class InMemoryRepository(Repository):
    """In-memory implementation of a repository for storing objects."""
    
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Adds an object to storage."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Fetches an object by its ID."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Returns all stored objects as a list."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Updates an object's attributes with new data."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key) and key not in ['id', 'created_at']:
                    setattr(obj, key, value)
            obj.save()  # Updates `updated_at` timestamp

    def delete(self, obj_id):
        """Removes an object from storage."""
        if obj_id in self._storage:
            del self._storage[obj_id]
