L.Polyline.include({
    _snakingTimestamp: 0,
    _snakingRings: 0,
    _snakingVertices: 0,
    _snakingDistance: 0,
    
    snakeIn: function () {
        if (this._snaking) { return; }

        this._snaking = true;
        this._snakingLayers = [];

        if (this._snakingTimestamp == 0) {
            this._snakingTimestamp = performance.now();
        }

        this._latlngs.forEach(latlng => {
            this._snakingLayers.push(latlng);
        });

        this._snakingRings = this._snakingLayers.length;
        this._snakingDistance = 0;

        for (var i = 0; i < this._snakingRings - 1; i++) {
            this._snakingDistance += this._snakingLayers[i].distanceTo(this._snakingLayers[i + 1]);
        }

        this._snakingVertices = 0;
        this._snake();
        this._map.on('zoomend', this._snakeZoom, this);
    },

    _snake: function () {
        if (!this._snaking) { return; }

        var now = performance.now();
        var elapsedTime = now - this._snakingTimestamp;

        var distance = elapsedTime * 0.1;

        if (distance >= this._snakingDistance) {
            this.setLatLngs(this._snakingLayers);
            this._snaking = false;
            this.fire('snakeend');
            return;
        }

        var pointIndex = this._snakingVertices;
        var currentPoint = this._snakingLayers[pointIndex];
        var nextPoint = this._snakingLayers[pointIndex + 1];

        var dist = currentPoint.distanceTo(nextPoint);

        if (distance >= dist) {
            this._snakingVertices++;
            distance -= dist;
            this._snake();
        } else {
            var ratio = distance / dist;
            var interpolatedPoint = [
                currentPoint.lat + (nextPoint.lat - currentPoint.lat) * ratio,
                currentPoint.lng + (nextPoint.lng - currentPoint.lng) * ratio
            ];

            var currentLatLngs = this._snakingLayers.slice(0, pointIndex + 1).concat([interpolatedPoint]);
            this.setLatLngs(currentLatLngs);

            L.Util.requestAnimFrame(this._snake, this);
        }
    },

    _snakeZoom: function () {
        if (this._snaking) {
            this._map.removeLayer(this);
            this._map.addLayer(this);
            this._snake();
        }
    }
});
